"""
main.py
-------
FastAPI app exposing:
- POST /upload  -> ingest a PDF into the vector store
- POST /chat    -> ask a question, get a streamed answer

Run with: uvicorn main:app --reload
"""

import os
import shutil
import tempfile
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from chroma_utils import add_pdf
from rag_chain import stream_answer

app = FastAPI(title="College Enquiry Chatbot")

# Allow the React dev server (running on port 5173) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    query: str


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Accepts a PDF, chunks it, embeds it, and stores it in ChromaDB."""
    if not file.filename.lower().endswith(".pdf"):
        return {"error": "Only PDF files are supported right now."}

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        num_chunks = add_pdf(tmp_path, source_name=file.filename)
    finally:
        os.remove(tmp_path)

    return {"filename": file.filename, "chunks_added": num_chunks}


@app.post("/chat")
async def chat(request: ChatRequest):
    """Streams the answer back token by token as it's generated."""
    if not request.query.strip():
        return {"error": "Query cannot be empty."}

    return StreamingResponse(
        stream_answer(request.query),
        media_type="text/plain",
    )


@app.get("/health")
async def health():
    return {"status": "ok"}