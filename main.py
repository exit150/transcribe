from typing import Annotated
import requests
from fastapi import FastAPI, File, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins = [
    "http://localhost:3000",
    "https://ai-lyriks.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def segments_to_srt(segments):
    srt_content = ""  # Initialize an empty string to store the SRT content

    for segment in segments:
        startTime = str(0) + str(timedelta(seconds=int(segment['start']))) + ',000'
        endTime = str(0) + str(timedelta(seconds=int(segment['end']))) + ',000'
        text = segment['text']
        segmentId = segment['id'] + 1
        segment_srt = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"
        srt_content += segment_srt  # Append each segment's SRT content to the main string

    print("SRT content generated successfully")
    return srt_content  # Return the accumulated SRT content directly


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/transcribe")
@limiter.limit("1/minute")
async def create_file(request: Request,file: Annotated[bytes, File()]):
    headers = {
        'Authorization': 'Bearer ' + os.getenv('OPENAI_API_KEY'),
        # requests won't add a boundary if this header is set when you pass files=
        # 'Content-Type': 'multipart/form-data',
    }

    files = {
        'file': ('audio.mp3', file),
        'timestamp_granularities[]': (None, 'segment'),
        'model': (None, 'whisper-1'),
        'response_format': (None, 'verbose_json'),
    }
    
    response = requests.post('https://api.openai.com/v1/audio/transcriptions', headers=headers, files=files)
    response_segments = response.json()["segments"]
    srt = segments_to_srt(response_segments)
    
    return {"srt": srt}
