from fastapi import FastAPI,Query,HTTPException,Body,Response
from fastapi import UploadFile, File, Form
from utils.youtube_transcript import get_transcripts
from youtube_transcript_api._errors import IpBlocked, NoTranscriptFound
from pydantic import BaseModel
from typing import List, Optional
from services.media_summariser.embed import create_embeddings
from services.YT_summarizer import summarize_long_transcript
from database.historySchema import NoteModel,NoteResponseModel
from database.crud import create_note
import tempfile
from services.PDF_summarizer import summarize_long_pdf
import os
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
    print("heelloo strating")
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
            print("embedding types",type(embeddings))
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
            "id": response_note.get("id"),
        }

    except Exception as e:
        return {"error": str(e)}


# --------------------------
# Summarize & Save Note PDF
# --------------------------
@app.post("/summarize-pdf")
async def summarize_PDF_and_save(
        file: UploadFile = File(...),
        user_id: str = Form(...),
        type: str = Form("PDF")
):
    try:

        from langchain_community.document_loaders import PyPDFLoader
        temp_pdf_path = None
        try:
            if not file.filename:
                return {"error": "File name is required"}
            pdf_bytes = await file.read()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                temp_pdf.write(pdf_bytes)
                temp_pdf_path = temp_pdf.name
            print("path of pdf :", temp_pdf_path)
            pdf_name = file.filename
            loader = PyPDFLoader(temp_pdf_path)
            pdf_docs = loader.load()
            pdf_text_only = [doc.page_content for doc in pdf_docs]

            clean_text = "".join(pdf_text_only)
            clean_text = clean_text.replace("\n", " ")
        finally:
            if temp_pdf_path and os.path.exists(temp_pdf_path):
                try:
                    os.remove(temp_pdf_path)
                except OSError:
                    pass

        summary = await summarize_long_pdf(pdf_docs)

        embedding_reference = None
        embeddings = None
        try:
            embeddings = create_embeddings(clean_text)
            if embeddings:
                import uuid
                embedding_reference = f"yt_{uuid.uuid4().hex[:8]}"
                print(f"✓ Embeddings created successfully with reference: {embedding_reference}")
            else:
                print("⚠ Embeddings returned None, proceeding without embedding storage")
        except Exception as embedding_error:
            print(f"⚠ Error creating embeddings: {str(embedding_error)}")

        note_data = NoteModel(
            user_id=user_id,
            title=pdf_name,
            type=type,
            summary=summary,
            pdf_content=pdf_text_only,
            source="Uploaded PDF",
            embeddings=embeddings
        )

        saved_note = create_note(note_data)
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

