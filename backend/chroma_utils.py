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

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")
COLLECTION_NAME = "college_docs"

# chunk_size: characters per chunk. Larger chunks keep more context together
# (e.g. a full fee table or admission step list) so answers don't get cut off.
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=200,
)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def get_vectorstore():
    """Returns a persistent Chroma vectorstore instance (loads existing data if present)."""
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )


def add_document(file_path: str, source_name: str):
    """
    Loads a PDF or TXT file, splits it into chunks, embeds each chunk,
    and stores it in Chroma.
    """
    if file_path.lower().endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.lower().endswith(".txt"):
        loader = TextLoader(file_path, encoding="utf-8")
    else:
        return 0

    pages = loader.load()
    chunks = splitter.split_documents(pages)

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