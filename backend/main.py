from fastapi import FastAPI,Query,HTTPException,Body,Response
from utils.youtube_transcript import get_transcripts
from youtube_transcript_api._errors import IpBlocked, NoTranscriptFound
from pydantic import BaseModel
from typing import List, Optional
app=FastAPI()

# Request Schemas
class YouTubeRequest(BaseModel):
    url: str


class TranscriptItem(BaseModel):
    time: str
    text: str


class SummarizeRequest(BaseModel):
    user_id: str
    title: str
    type: str = "youtube"
    url: Optional[str] = None
    transcript: Optional[List[TranscriptItem]] = None


class FlashcardRequest(BaseModel):
    summary: str


class ChatRequest(BaseModel):
    message: str
    summary: Optional[str] = None
    videoId: str



# --------------------------
# YouTube Transcript API route for viewPage component transcript displaying
# --------------------------

@app.get("/transcript/")
def transcript_api(url: str):
    try:
        transcripts = get_transcripts(url)
        return {"transcript": transcripts}
    except IpBlocked:
        return {"error": "Your IP is blocked by YouTube. Try again later or from a different network."}
    except NoTranscriptFound:
        return {"error": "Transcript not found for this video."}
    except Exception as e:
        return {"error": str(e)}



