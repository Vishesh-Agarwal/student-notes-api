from fastapi import FastAPI, Depends, HTTPException
from schemas import Note
from database import engine, Base
from models import NoteDB, UserDB
from sqlalchemy.orm import Session
from dependencies import get_db

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Student Notes API"}

@app.post("/notes/")
def create_note(note: Note, db: Session = Depends(get_db)):
    db_note = NoteDB(
    title=note.title,
    content=note.content
    )

    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return {
        "message": "Note created successfully",
        "note": db_note
    }

@app.get("/notes/")
def get_notes(db: Session = Depends(get_db)):
    note = db.query(NoteDB).all()
    return {"notes": note}

@app.get("/notes/{note_id}")
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(NoteDB).filter(NoteDB.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"note": note}

@app.put("/notes/{note_id}")
def update_note(note_id: int, updated_note: Note, db: Session = Depends(get_db)):
    note = db.query(NoteDB).filter(NoteDB.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note.title = updated_note.title
    note.content = updated_note.content
    db.commit()
    db.refresh(note)
    return {
        "message": "Note updated successfully",
                "note": note
            }

@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(NoteDB).filter(NoteDB.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()
    return {"message": "Note deleted successfully"}