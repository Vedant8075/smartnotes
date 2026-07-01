from database.historySchema import NoteModel
from datetime import datetime
from database.config import client
from bson.objectid import ObjectId

db = client.notesDB
notes_collection = db.get_collection("notes")

# Helper to convert MongoDB document to dict
def note_helper(note) -> dict:
    return {
        "id": str(note["_id"]),
        "user_id": note["user_id"],
        "title": note.get("title"),
        "type": note.get("type"),
        "summary": note.get("summary"),
        "transcript": note.get("transcript"),
        "media_content": note.get("media_content"),
        "pdf_content": note.get("pdf_content"),
        "chat_content": note.get("chat_content"),
        "embeddings": note.get("embeddings"),
        "source": note.get("source"),
        "created_at": note.get("created_at"),
    }

def create_note(note: NoteModel):
    note_dict = note.dict(exclude_none=True)
    note_dict["created_at"] = datetime.utcnow()

    result = notes_collection.insert_one(note_dict)
    created_note = notes_collection.find_one({"_id": result.inserted_id})
    
    return note_helper(created_note)