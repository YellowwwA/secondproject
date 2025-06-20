from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from elevenlabs import ElevenLabs, VoiceSettings
import boto3
import io
import re
from datetime import datetime


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 중에는 *로 두세요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("ELEVENLABS_API_KEY")
AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME=os.getenv("S3_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION")

client = ElevenLabs(api_key=API_KEY)

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)


VOICE_ID = "ksaI0TCD9BstzEzlxj4q"

def generate_unique_mp3_key():
    date_str = datetime.now().strftime("%Y-%m-%d")
    base_filename = f"tts_meeting_{date_str}"
    folder = f"tts_meeting/"

    existing = s3.list_objects_v2(
        Bucket=S3_BUCKET_NAME,
        Prefix=folder + base_filename
    )

    suffix = 0
    if "Contents" in existing:
        pattern = re.compile(f"{base_filename}(?:_(\\d+))?\\.mp3$")
        for obj in existing["Contents"]:
            key = obj["Key"].split("/")[-1] # abc_2025-06-20_1.txt
            match = pattern.match(key)
            if match and match.group(1):
                suffix = max(suffix, int(match.group(1)))
        suffix += 1
        filename = f"{base_filename}_{suffix}.mp3"
    else:
        filename = f"{base_filename}.mp3"

    return f"{folder}{filename}"


def read_text_file(s3_key: str) -> str:
    response = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix="generate_meeting/generate_meeting")
    if "Contents" not in response:
        return {"error"}
    
    #최신 파일 찾기
    latest_file = max(response["Contents"], key=lambda x: x["LastModified"])
    key = latest_file["Key"]
    
    #S3에서 해당 파일 읽기
    file_obj = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=key)
    text_content = file_obj["Body"].read().decode("utf-8")
    
    return text_content
    
    
def text_to_speech(text: str):
    # 음성 생성 요청
    response = client.text_to_speech.convert(
        voice_id=VOICE_ID,
        text=text,
        model_id="eleven_flash_v2_5",
        output_format="mp3_44100_128",
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.75
        )
    )
    
    # 응답 받은 오디오 데이터를 파일로 저장
    # with open(output_path, "wb") as f:
    #     for chunk in response:
    #         if chunk:
    #             f.write(chunk)
    
    s3_key = generate_unique_mp3_key()
    mp3_stream = io.BytesIO(response.content)
    s3.upload_fileobj(mp3_stream, S3_BUCKET_NAME, s3_key)

    return "음성 파일 저장완료"


@app.get('/')
async def tts_meeting():
    text = read_text_file()
    text_to_speech(text)
    return {"TTS완료"}
    
    
