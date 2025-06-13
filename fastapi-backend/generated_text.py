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
@app.get("/")
async def Getroot():
    return "Helloworld"

@app.get("/test")
async def GetTest():
    result = "test"
    return result

@app.get('/generate_meeting')
async def generate_meeting(keyword: str, num: int, textlength: int):
    
    if (keyword is None) or (num is None):
        return "키워드와 화자 수를 입력하세요.@@"

    prompt = f'''대화형식으로 대본을 써주세요
    '{keyword}'회사에서 '{num}'명의 직원이 진행한 회의를 대화하는 형식으로 '{textlength}'단어 분량으로 만들어줘.'''

    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0.7,
        max_tokens=textlength
    )
    result = response.choices[0].text.strip()
    result = result.replace('\n\n', '\n')
    result = result.replace('\n', ' ')
    
    file_path = "generated_meetingtext.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(result)
    
    return {result}