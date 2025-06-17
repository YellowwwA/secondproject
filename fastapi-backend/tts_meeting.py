from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from elevenlabs import ElevenLabs, VoiceSettings
import subprocess
import base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 중에는 *로 두세요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("ELEVENLABS_API_KEY")

client = ElevenLabs(api_key=API_KEY)

VOICE_ID = "ksaI0TCD9BstzEzlxj4q"


# @app.get("/")
# async def Getroot():
#     return "HelloworldTTS"

@app.get('/')
async def tts_meeting():
    text_file_path = "generated_meetingtext.txt"      # 읽을 텍스트 파일
    output_audio_path = "meetingaudio.mp3"  # 저장할 mp3 파일

    text = read_text_file(text_file_path)
    text_to_speech(text, output_audio_path)
    return {"TTS완료"}



def read_text_file(s3_key: str) -> str:
    result = subprocess.run(
        ["node", "../node-backend/download.js", s3_key, "text"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,          # stdout, stderr을 str로 자동 디코딩
        check=True
    )
    return result.stdout
    
    
def text_to_speech(text: str, output_path: str):
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
    
    mp3_bytes = response  # bytes라면 바로 이걸로 됨
    mp3_base64 = base64.b64encode(mp3_bytes).decode("utf-8")
    subprocess.run(["node", "../node-backend/upload.js", "mp3", mp3_base64],
                   text=True,
                   check=True
    )
                

    return "음성 파일 저장완료"
    
    
