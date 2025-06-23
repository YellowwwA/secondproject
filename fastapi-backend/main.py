from fastapi import FastAPI
from generate_meeting import app as generate_meeting
from stt_meeting import app as stt_meeting
from tts_meeting import app as tts_meeting
from summarize_meetingtext import app as summarize_meetingtext
from search_meeting import app as search_meeting

app = FastAPI()

app.mount("/generate_meeting", generate_meeting)
app.mount("/stt_meeting", stt_meeting)
app.mount("/tts_meeting", tts_meeting)
app.mount("/summarize_meetingtext", summarize_meetingtext)
app.mount("/search_meeting", search_meeting)