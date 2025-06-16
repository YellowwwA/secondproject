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
#     return "Helloworld"


@app.get('/')
async def summarize_meeting():
    with open("generated_meetingtext.txt", "r", encoding="utf-8") as f:
        text = f.read()

    prompt = f'''다음 텍스트를 요약해줘 \n\n{text}
    '''
    response = openai.Completion.create(
    model="gpt-3.5-turbo-instruct",
    prompt=prompt,
    temperature=0,
    max_tokens=100
    )

    summary = response.choices[0].text.strip()
    with open("summarizemeetingtext.txt", "w", encoding="utf-8") as f:
        f.write(summary)
        
    print("요약 완료")
    return {summary}