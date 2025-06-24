import os
import json
import re
import faiss
import numpy as np
import openai

openai.api_key=os.getenv("OPENAI_API_KEY")
print("Current working directory:", os.getcwd())
EC2_DIR = "./faiss"
INDEX_PATH = os.path.join(EC2_DIR, "index.faiss")
MAPPING_PATH = os.path.join(EC2_DIR, "id_to_s3.json")



# 텍스트를 화자 기준으로 나눔
def split_by_speaker(text):
    pattern = r'([A-Z]:)'  # 화자 패턴 (예: A:, B:, ...)
    parts = re.split(pattern, text)
    chunks = []
    for i in range(1, len(parts), 2):
        speaker = parts[i].strip()
        utterance = parts[i+1].strip() if (i+1) < len(parts) else ''
        chunks.append(f"{speaker} {utterance}")
    if not chunks:
        return [text]
    return chunks

# 임베딩 생성
def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    embedding = response['data'][0]['embedding']
    return np.array(embedding, dtype='float32')

def embeddingfaiss(text, s3_file_key):
    # 텍스트 분할
    chunks = split_by_speaker(text)
    print("Chunks:", chunks)

    # 임베딩 생성
    embedding_vectors = []
    for chunk in chunks:
        emb = get_embedding(chunk)
        print("Embedding shape:", emb.shape)
        embedding_vectors.append(emb)
    embedding_vectors = np.vstack(embedding_vectors)

    # FAISS 인덱스 로드 또는 생성
    if os.path.exists(INDEX_PATH):
        index = faiss.read_index(INDEX_PATH)
    else:
        dim = embedding_vectors.shape[1]
        index = faiss.IndexFlatL2(dim)

    # 매핑 로드 또는 새로 생성
    if os.path.exists(MAPPING_PATH):
        with open(MAPPING_PATH, "r") as f:
            id_to_s3 = json.load(f)
        id_to_s3 = {int(k): v for k, v in id_to_s3.items()}
    else:
        id_to_s3 = {}

    # 벡터 추가 및 매핑 저장
    start_id = index.ntotal
    index.add(embedding_vectors)

    for i in range(len(chunks)):
        vid = start_id + i
        id_to_s3[vid] = f"{s3_file_key}#chunk{i}"

    faiss.write_index(index, INDEX_PATH)
    with open(MAPPING_PATH, "w") as f:
        json.dump(id_to_s3, f)

    print(f"FAISS index and mapping saved to {EC2_DIR}")
    
def search_faiss(keyword, top_k=3):
    # 1. FAISS 인덱스와 매핑 파일 존재 여부 확인
    if not os.path.exists(INDEX_PATH):
        raise FileNotFoundError(f"FAISS index file not found at {INDEX_PATH}")
    if not os.path.exists(MAPPING_PATH):
        raise FileNotFoundError(f"Mapping file not found at {MAPPING_PATH}")

    # 2. 인덱스와 매핑 로드
    index = faiss.read_index(INDEX_PATH)

    with open(MAPPING_PATH, "r") as f:
        id_to_s3 = json.load(f)
    id_to_s3 = {int(k): v for k, v in id_to_s3.items()}

    # 3. 키워드 임베딩 생성
    try:
        query_vec = get_embedding(keyword).reshape(1, -1)
    except Exception as e:
        print(f"[Embedding Error] {e}")
        return []

    # 4. 검색 수행
    try:
        distances, indices = index.search(query_vec, top_k)
    except Exception as e:
        print(f"[FAISS Search Error] {e}")
        return []

    # 5. 결과 구성
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue  # 안전하게 체크, 대부분 불필요하지만 유지 가능
        s3_path = id_to_s3.get(idx, "Unknown")
        results.append({
            "faiss_id": idx,
            "distance": float(dist),
            "s3_path": s3_path
        })

    return results

# if __name__ == "__main__":
#     filename = "generated_meetingtext.txt"  # 같은 폴더에 있는 텍스트 파일 이름
#     with open(filename, "r", encoding="utf-8") as f:
#         file_text = f.read()
#     sample_s3_key = "./abc.txt"
    
#     embeddingfaiss(file_text, sample_s3_key)