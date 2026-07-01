from database.historySchema import NoteModel
from datetime import datetime

db = client.notesDB
notes_collection = db.get_collection("notes")

def create_note(note: NoteModel):
    note_dict = note.dict(exclude_none=True)
    note_dict["created_at"] = datetime.utcnow()

    result = notes_collection.insert_one(note_dict)
    created_note = notes_collection.find_one({"_id": result.inserted_id})
    
    return note_helper(created_note)