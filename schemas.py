from pydantic import BaseModel, Field

class Note(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    content: str = Field(min_length=5, max_length=200)
    user_id: int

class User(BaseModel):
    username: str = Field(min_length=3, max_length=20)