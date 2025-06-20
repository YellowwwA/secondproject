from fastapi import FastAPI
from pydantic import BaseModel
import openai
from fastapi.middleware.cors import CORSMiddleware
import os
import io
import boto3
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 중에는 *로 두세요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key=os.getenv("OPENAI_API_KEY")
AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME=os.getenv("S3_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

def sttmeeting_s3_key():
    date_str = datetime.now().strftime("%Y-%m-%d")
    base_filename = f"stt_meeting_{date_str}"
    folder = "stt_meeting/"
    existing_files = s3.list_objects_v2(
        Bucket=S3_BUCKET_NAME,
        Prefix=folder + base_filename
    )
    suffix = 0
    if "Contents" in existing_files:
        pattern = re.compile(f"{base_filename}(_(\\d+))?\\.txt$")
        for obj in existing_files["Contents"]:
            key = obj["Key"].split("/")[-1]  # abc_2025-06-20_1.txt
            match = pattern.match(key)
            if match and match.group(2):
                suffix = max(suffix, int(match.group(2)))
        
        suffix += 1
        filename = f"{base_filename}_{suffix}.txt"
    else:
        filename = f"{base_filename}.txt"
                
    return f"{folder}/{filename}"

def read_transcribe_mp3(s3_key: str):
    # S3에서 mp3 파일 가져오기
    response = s3.get_object(Bucket=S3_BUCKET_NAME, Key=s3_key)
    audio_stream = response["Body"].read()  # MP3 바이너리
    # BytesIO로 메모리 내 파일 객체 만들기
    audio_file = io.BytesIO(audio_stream)
    audio_file.name = "audio.mp3"
    
    transcript = openai.Audio.transcribe(model="whisper-1", file=audio_file)
    return transcript["text"]
    

@app.get('/')
async def stt_meeting():
    response = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix="tts_meeting/tts_meeting")
    if "Contents" not in response:
        return {"error": "파일 없음"}

    latest_file = max(response["Contents"], key=lambda x: x["LastModified"])
    s3_keyA = latest_file["Key"]
    
    result = read_mp3_from_s3(s3_keyA)
    
    #파일로 변환 후 s3업로드
    file_stream = io.BytesIO(result.text.encode("utf-8"))
    s3_key = sttmeeting_s3_key()
    s3_client.upload_fileobj(file_stream, S3_BUCKET_NAME, s3_key)    

    print(transcript.text)
    return(transcript.text)