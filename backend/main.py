from fastapi import FastAPI,Query,HTTPException,Body,Response
from utils.youtube_transcript import get_transcripts
from youtube_transcript_api._errors import IpBlocked, NoTranscriptFound
from pydantic import BaseModel
from typing import List, Optional
from services.media_summariser.embed import create_embeddings
from services.YT_summarizer import summarize_long_transcript

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



# --------------------------
# Summarize & Save Note YOUTUBE
# --------------------------
@app.post("/summarize-yt")
async def summarize_youtube_and_save(req: SummarizeRequest):
    try:
        if req.transcript:
            transcripts = [item.dict() for item in req.transcript]
        elif req.url:
            transcripts = get_transcripts(req.url)
        else:
            return {"error": "Provide either a transcript or a URL"}

        text_for_embedding = " ".join([item["text"] for item in transcripts])

        summary = await summarize_long_transcript(transcripts)

        embedding_reference = None
        embeddings = None
        try:
            embeddings = create_embeddings(text_for_embedding)
            if embeddings:
                import uuid
                embedding_reference = f"yt_{uuid.uuid4().hex[:8]}"
                print(f"✓ Embeddings created successfully with reference: {embedding_reference}")
            else:
                print("⚠ Embeddings returned None, proceeding without embedding storage")
        except Exception as embedding_error:
            print(f"⚠ Error creating embeddings: {str(embedding_error)}")

        note_data = NoteModel(
            user_id=req.user_id,
            title=req.title,
            type=req.type,
            summary=summary,
            transcript=transcripts,
            source=req.url or "uploaded transcript",
            embeddings=embeddings
        )

        saved_note = create_note(note_data)

        # Avoid returning potentially large embeddings payload to the frontend.
        response_note = dict(saved_note)
        response_note.pop("embeddings", None)

        return {
            "summary": summary,
            "note": response_note,
            "embeddings_status": "success" if embedding_reference else "skipped",
            "id": saved_note.get("_id")
        }

    except Exception as e:
        return {"error": str(e)}

