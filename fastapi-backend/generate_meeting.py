from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
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

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# @app.get("/")
# async def Getroot():
#     return "Helloworld"

# @app.get("/testGT")
# async def GetTestGT():
#     result = "test Generated Text"
#     return result

@app.get('/')
async def generate_meeting(keyword: str, num: int, textlength: int):
    
    if (keyword is None) or (num is None):
        return "키워드와 화자 수를 입력하세요.@@"

    prompt = f'''대화형식으로 대본을 써주세요
    '{keyword}'회사에서 '{num}'명의 직원이 진행한 회의를 대화하는 형식으로 '{textlength}'단어 분량으로 만들어줘.'''

    response = client.Completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0.7,
        max_tokens=textlength
    )
    result = response.choices[0].text.strip()
    result = result.replace('\n\n', '\n')
    result = result.replace('\n', ' ')
    
    # file_path = "generated_meetingtext.txt"
    # with open(file_path, "w", encoding="utf-8") as f:
    #     f.write(result)
    
    filename = "generated_meetingtext.txt"
    subprocess.run(["node", "../node-backend/upload.js","text", filename, result])
    
    return {result}
    
