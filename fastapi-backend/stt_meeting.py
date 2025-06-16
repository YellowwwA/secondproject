from fastapi import FastAPI
from pydantic import BaseModel
import openai 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 중에는 *로 두세요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/")
# async def Getroot():
#     return "HelloworldSTT"

@app.get('/')
async def stt_meeting():
    audio_file = open("meetingaudio.mp3", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    file_path = "STT_meetingtext.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(transcript.text)

    print(transcript.text)
    return(transcript.text)