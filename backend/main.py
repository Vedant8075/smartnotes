from fastapi import FastAPI,Query,HTTPException,Body,Response
from utils.youtube_transcript import get_transcripts
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


