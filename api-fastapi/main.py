import os
import mysql.connector
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppass")
DB_NAME = os.getenv("DB_NAME", "notesdb")

def conn():
    return mysql.connector.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )

def init_db():
    c = conn()
    cur = c.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes(
          id INT AUTO_INCREMENT PRIMARY KEY,
          content TEXT NOT NULL,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.commit()
    cur.close()
    c.close()

@app.on_event("startup")
def startup():
    init_db()

@app.get("/api/health")
def health():
    return {"ok": True}

@app.get("/api/notes")
def list_notes():
    c = conn()
    cur = c.cursor(dictionary=True)
    cur.execute("SELECT id, content, created_at FROM notes ORDER BY id DESC LIMIT 50")
    rows = cur.fetchall()
    cur.close()
    c.close()
    return rows

class NoteIn(BaseModel):
    content: str

@app.post("/api/notes", status_code=201)
def add_note(body: NoteIn):
    content = (body.content or "").strip()
    if not content:
        return {"message": "content is required"}
    c = conn()
    cur = c.cursor(dictionary=True)
    cur.execute("INSERT INTO notes(content) VALUES(%s)", (content,))
    c.commit()
    note_id = cur.lastrowid
    cur.execute("SELECT id, content, created_at FROM notes WHERE id=%s", (note_id,))
    row = cur.fetchone()
    cur.close()
    c.close()
    return row
