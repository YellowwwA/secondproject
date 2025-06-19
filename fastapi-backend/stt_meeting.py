from fastapi import FastAPI
from pydantic import BaseModel
import openai 
from fastapi.middleware.cors import CORSMiddleware
import os
import subprocess
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 중에는 *로 두세요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# @app.get("/")
# async def Getroot():
#     return "HelloworldSTT"

@app.get('/')
async def stt_meeting():
    result = subprocess.run(
    ["node", "../node-backend/download.js", "meetingaudio.mp3", "mp3"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    check=True
    )
    mp3_bytes = result.stdout
    audio_file = io.BytesIO(mp3_bytes)
    audio_file.name = "meetingaudio.mp3 "
    
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)

    filename = "STT_meetingtext.txt"
    subprocess.run(["node", "../node-backend/upload.js","text", filename, result])

    print(transcript.text)
    return(transcript.text)