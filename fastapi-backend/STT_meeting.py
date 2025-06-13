import openai 

audio_file = open("meetingaudio.mp3", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)

file_path = "STT_meetingtext.txt"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(transcript.text)

print(transcript.text)