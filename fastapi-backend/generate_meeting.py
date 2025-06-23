from fastapi import FastAPI
from pydantic import BaseModel
import openai
from fastapi.middleware.cors import CORSMiddleware
import os
import io
import boto3
from datetime import datetime
import re
import faiss
import numpy as np
import json
from embedding import embeddingfaiss

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

def generate_s3_key():
    date_str = datetime.now().strftime("%Y-%m-%d")
    base_filename = f"generate_meeting_{date_str}"
    folder = "generate_meeting/"
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
    
    #s3에 저장할수있게 파일로 변환
    file_stream = io.BytesIO(result.encode("utf-8"))
    s3_key = generate_s3_key()
    s3_client.upload_fileobj(file_stream, S3_BUCKET_NAME, s3_key)
    
    #임베딩하여 FAISSDB에 저장
    embeddingfaiss(result, s3_key)
    
    return {result}
    
