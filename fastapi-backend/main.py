from fastapi import FastAPI
from generate_meeting import app as generate_meeting
from stt_meeting import app as stt_meeting
from tts_meeting import app as tts_meeting
from summarize_meetingtext import app as summarize_meetingtext
from search_meeting import app as search_meeting
from faiss_manager import download_faiss_from_s3, upload_faiss_to_s3

app = FastAPI()

@app.on_event("startup")
def startup_event():
    download_faiss_from_s3()  # 실행 시 최신 인덱스를 받아옴

app.mount("/generate_meeting", generate_meeting)
app.mount("/stt_meeting", stt_meeting)
app.mount("/tts_meeting", tts_meeting)
app.mount("/summarize_meetingtext", summarize_meetingtext)
app.mount("/search_meeting", search_meeting)