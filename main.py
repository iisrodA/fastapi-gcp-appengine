import os

from dotenv import load_dotenv
from fastapi import FastAPI
from google.cloud import firestore
from pydantic import BaseModel

load_dotenv()

credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if credentials_path:
    os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", credentials_path)

project_id = os.getenv("PROJECT_ID")
database_id = os.getenv("DATABASE_ID")

db = firestore.Client(project=project_id, database=database_id)

app = FastAPI()


class NoteCreate(BaseModel):
    title: str
    content: str


@app.get("/")
def read_root():
    return {"Hello": "Este es otro servicio"}


@app.post("/create")
def create_something(note: NoteCreate):
    ref = db.collection("examples").document()

    ref.set({
        "title": note.title,
        "content": note.content,
    })
    return {"msg": "created"}