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
MODEL_NAME = "openai/gpt-oss-20b"

RELEVANCE_THRESHOLD = 0.25

SYSTEM_PROMPT = """You are a helpful, friendly college enquiry assistant for Vidya Jyothi Institute of Technology.
You're chatting with a student, so answer naturally and conversationally.

Guidelines:
- Never mention "point 11", "the context", "the document", section numbers, or table structure.
- Rewrite information in your own words. Don't copy raw formatting or numbering from source material.
- Be direct and complete.
- If some details are missing, answer with what you know and suggest confirming with the admissions office.
- Keep the tone warm and helpful.

Here's what you know that's relevant to the student's question:
{context}
"""


def build_prompt(query: str):
    results = query_chunks(query, k=6)

    if not results:
        return None, []

    # Note: Sentence-Transformers' relevance scores through LangChain/Chroma
    # come out miscalibrated (negative values) for this embedding backend —
    # a known compatibility quirk. Rather than filter on a broken score,
    # we trust the top-k semantic ranking directly, which is reliable even
    # though the raw numbers aren't.
    context_text = "\n\n---\n\n".join(doc.page_content for doc, _ in results)
    sources = list({doc.metadata.get("source", "unknown") for doc, _ in results})
    system_message = SYSTEM_PROMPT.format(context=context_text)
    return system_message, sources


def stream_answer(query: str):
    system_message, sources = build_prompt(query)

    if system_message is None:
        yield "I don't have that information right now — you might want to check with the admissions office directly."
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