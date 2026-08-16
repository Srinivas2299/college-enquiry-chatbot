"""
chroma_utils.py
----------------
Handles everything related to the vector store:
- splitting documents into chunks
- embedding them (turning text into number vectors that capture meaning)
- storing/retrieving from ChromaDB
"""

import os
os.environ["HF_HUB_OFFLINE"] = "1"

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")
COLLECTION_NAME = "college_docs"

# chunk_size: characters per chunk. Too big -> irrelevant text mixed in.
# Too small -> answers get cut across chunk boundaries and lose context.
# chunk_overlap: shared characters between consecutive chunks so a sentence
# straddling a boundary isn't lost.
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
)

# Runs locally on your machine, completely free, no API key needed.
# Downloads the model (~90MB) once on first run, then it's cached.
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def get_vectorstore():
    """Returns a persistent Chroma vectorstore instance (loads existing data if present)."""
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )


def add_pdf(file_path: str, source_name: str):
    """
    Loads a PDF, splits it into chunks, embeds each chunk, and stores it in Chroma.
    """
    loader = PyPDFLoader(file_path)
    pages = loader.load()

    chunks = splitter.split_documents(pages)

    # Skip PDFs with no extractable text (e.g. scanned image-only PDFs)
    if len(chunks) == 0:
        return 0

    for chunk in chunks:
        chunk.metadata["source"] = source_name

    vectorstore = get_vectorstore()
    vectorstore.add_documents(chunks)
    return len(chunks)

def query_chunks(query: str, k: int = 4):
    """
    Given a user question, returns the top-k most semantically similar chunks
    from the vector store, along with their similarity scores.
    """
    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search_with_relevance_scores(query, k=k)
    return results