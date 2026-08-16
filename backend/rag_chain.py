"""
rag_chain.py
------------
The "generation" half of RAG: takes retrieved chunks + the user's question,
builds a prompt, and streams a response back from the LLM (via Groq, free tier).
"""

import os
from dotenv import load_dotenv

load_dotenv()

from groq import Groq
from chroma_utils import query_chunks

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL_NAME = "llama-3.1-8b-instant"

# Below this similarity score, we don't trust the retrieved chunks enough
# to answer from them. Tune this after testing with real questions.
RELEVANCE_THRESHOLD = 0.3

SYSTEM_PROMPT = """You are a helpful college enquiry assistant for Vidya Jyothi Institute of Technology.
Answer the student's question using ONLY the context provided below.
If the context does not contain the answer, say you don't have that information
and suggest they contact the admissions office — do not make anything up.

Context:
{context}
"""


def build_prompt(query: str):
    """Retrieves relevant chunks and assembles the final prompt sent to the LLM."""
    results = query_chunks(query, k=4)

    relevant = [(doc, score) for doc, score in results if score >= RELEVANCE_THRESHOLD]

    if not relevant:
        return None, []

    context_text = "\n\n---\n\n".join(doc.page_content for doc, _ in relevant)
    sources = list({doc.metadata.get("source", "unknown") for doc, _ in relevant})

    system_message = SYSTEM_PROMPT.format(context=context_text)
    return system_message, sources


def stream_answer(query: str):
    """
    Generator that yields response tokens as they arrive from the LLM.
    If no relevant context was found, yields a fallback message instead.
    """
    system_message, sources = build_prompt(query)

    if system_message is None:
        yield "I don't have information on that in my current documents. Please check with the admissions office."
        return

    stream = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": query},
        ],
        stream=True,
    )

    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta