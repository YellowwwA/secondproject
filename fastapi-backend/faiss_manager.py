import boto3, os


S3_BUCKET_NAME=os.getenv("S3_BUCKET_NAME")
AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

S3_FAISS_PREFIX = "faiss"
LOCAL_FAISS_DIR = "./faiss"
INDEX_FILE = "index.faiss"
MAPPING_FILE = "id_to_s3.json"

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)


def download_faiss_from_s3():
    os.makedirs(LOCAL_FAISS_DIR, exist_ok=True)
    for filename in [INDEX_FILE, MAPPING_FILE]:
        local_path = os.path.join(LOCAL_FAISS_DIR, filename)
        s3_key = f"{S3_FAISS_PREFIX}/{filename}"
        try:
            print(f"[Download] {s3_key} → {local_path}")
            s3_client.download_file(S3_BUCKET_NAME, s3_key, local_path)
        except Exception as e:
            print(f"[Warning] Failed to download {s3_key}: {e}")

def upload_faiss_to_s3():
    for filename in [INDEX_FILE, MAPPING_FILE]:
        local_path = os.path.join(LOCAL_FAISS_DIR, filename)
        s3_key = f"{S3_FAISS_PREFIX}/{filename}"
        try:
            print(f"[Upload] {local_path} → {s3_key}")
            s3_client.upload_file(local_path, S3_BUCKET_NAME, s3_key)
        except Exception as e:
            print(f"[Error] Failed to upload {filename}: {e}")