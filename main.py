from fastapi import FastAPI, Depends, HTTPException
from schemas import Note, User, UserCreate, UserLogin
from database import engine, Base
from models import NoteDB, UserDB
from sqlalchemy.orm import Session
from dependencies import get_db
from security import hash_password, verify_password, create_access_token


app = FastAPI()

@app.get("/")
def home():
    return {"message": "Student Notes API"}

@app.post("/users/")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    db_user = UserDB(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@app.post("/users/login")
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    db_user = (
        db.query(UserDB)
        .filter(UserDB.username == user.username)
        .first()
    )

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/notes/")
def create_note(note: Note, db: Session = Depends(get_db)):
    db_note = NoteDB(
    title=note.title,
    content=note.content,
    user_id=note.user_id
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

@app.get("/users/{user_id}/notes")
def get_user_notes(
    user_id: int,
    db: Session = Depends(get_db)
):
    notes = (
        db.query(NoteDB)
        .filter(NoteDB.user_id == user_id)
        .all()
    )

    return notes