from fastapi import FastAPI
from pydantic import BaseModel
import openai
from fastapi.middleware.cors import CORSMiddleware
import os
import io
import boto3
from datetime import datetime
import re
from embedding import embeddingfaiss, search_faiss

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



@app.get('/')
async def search_meeting(keyword: str):
    top_k = 3
    search_results = search_faiss(keyword, top_k)
    if not search_results:
        return {"message":"No search results found."}
    s3_path = search_results[0]["s3_path"]
    for r in search_results:
        print(f"FAISS ID: {r['faiss_id']}, Distance: {r['distance']:.4f}, S3 File & Chunk: {r['s3_path']}")

    origintext = get_text_from_s3(s3_path)
    return {
        "search_results": search_results,
        "original_text": origintext
    }

def get_text_from_s3(s3_path):
    s3_path = s3_path.split('#')[0]
    if '/' not in s3_path:
        raise ValueError(f"Invalid S3 path format: {s3_path}")
    
    bucket, key = s3_path.split('/', 1)
    
    print("S3 PATH:", s3_path)
    print("Bucket:", bucket)
    print("Key:", key)
    
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket, Key=key)
    return obj['Body'].read().decode('utf-8')