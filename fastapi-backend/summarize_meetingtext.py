from fastapi import FastAPI
from pydantic import BaseModel
import openai
from fastapi.middleware.cors import CORSMiddleware
import os
import subprocess

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
#     return "Helloworld"


@app.get('/')
async def summarize_meeting():
    result = subprocess.run(
        ["node", "../node-backend/download.js", "STT_meetingtext.txt", "text"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,          # stdout, stderr을 str로 자동 디코딩
        check=True
    )

    prompt = f'''다음 텍스트를 요약해줘 \n\n{result.stdout}
    '''
    response = openai.Completion.create(
    model="gpt-3.5-turbo-instruct",
    prompt=prompt,
    temperature=0,
    max_tokens=100
    )

    summary = response.choices[0].text.strip()
    
    filename = "summarizemeetingtext.txt"
    subprocess.run(["node", "../node-backend/upload.js","text", filename, result])
        
    print("요약 완료")
    return {summary}