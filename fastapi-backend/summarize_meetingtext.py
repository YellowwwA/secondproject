from fastapi import FastAPI
from pydantic import BaseModel
import openai
from fastapi.middleware.cors import CORSMiddleware
import os
import io
import boto3
from datetime import datetime
import re

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

def read_text_file():
    response = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix="stt_meeting/stt_meeting")
    if "Contents" not in response:
        return {"error"}
    
    #최신 파일 찾기
    latest_file = max(response["Contents"], key=lambda x: x["LastModified"])
    key = latest_file["Key"]
    
    #S3에서 해당 파일 읽기
    file_obj = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=key)
    text_content = file_obj["Body"].read().decode("utf-8")
    
    return text_content

def summarizemeeting_s3_key():
    date_str = datetime.now().strftime("%Y-%m-%d")
    base_filename = f"summarize_meetingtext_{date_str}"
    folder = "summarize_meetingtext/"
    existing_files = s3_client.list_objects_v2(
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
                
    return f"{folder}{filename}"


@app.get('/')
async def summarize_meeting(text: str):

    prompt = f'''다음 텍스트를 요약해줘 \n\n{text}
    '''
    response = openai.Completion.create(
    model="gpt-3.5-turbo-instruct",
    prompt=prompt,
    temperature=0,
    max_tokens=100
    )

    summary = response.choices[0].text.strip()
    
    file_stream = io.BytesIO(summary.encode("utf-8"))

    s3_key = summarizemeeting_s3_key()
    s3_client.upload_fileobj(file_stream, S3_BUCKET_NAME, s3_key)
    
    print("요약 완료")
    return {summary}