from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Note(BaseModel):
    id: int
    title: str
    content: str

notes = []

@app.get("/")
def home():
    return {"message": "Student Notes API"}

@app.post("/notes/")
def create_note(note: Note):
    notes.append(note)
    return {
        "message": "Note created successfully",
        "note": note
    }

@app.get("/notes/")
def get_notes():
    return {"notes": notes}

@app.get("/notes/{note_id}")
def get_note(note_id: int):
    for note in notes:
        if note.id == note_id:
            return {"note": note}
    return {"message": "Note not found"}

@app.put("/notes/{note_id}")
def update_note(note_id: int, updated_note: Note):
    for index, note in enumerate(notes):
        if note.id == note_id:
            notes[index] = updated_note
            return {
                "message": "Note updated successfully",
                "note": updated_note
            }
    return {"message": "Note not found"}

@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    for index, note in enumerate(notes):
        if note.id == note_id:
            del notes[index]
            return {"message": "Note deleted successfully"}
    return {"message": "Note not found"}