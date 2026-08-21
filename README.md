# VJIT College Enquiry Chatbot

An AI-powered college enquiry chatbot for **Vidya Jyothi Institute of Technology (VJIT)** that uses **Retrieval-Augmented Generation (RAG)** to provide accurate, context-aware answers from a college-specific knowledge base.

The system retrieves relevant information from indexed VJIT documents and passes it to an LLM to generate concise and conversational responses.

## Overview

Students often need information about college facilities, fees, placements, courses, and other academic or administrative details. Instead of manually searching through multiple documents, this chatbot provides a single conversational interface for answering such queries.

The application combines **semantic search and LLM-based generation** so that responses are grounded in the available VJIT information rather than relying only on the model's general knowledge.

## Key Features

* Retrieval-Augmented Generation (RAG) based question answering
* Semantic document retrieval using vector embeddings
* Chroma-based vector storage and retrieval
* Groq LLM integration for response generation
* VJIT-specific knowledge base
* Concise and conversational responses
* Markdown rendering for formatted responses
* Responsive React-based chat interface
* Separation of frontend, backend, retrieval, and generation components

## System Architecture

```text
                    User
                      │
                      ▼
              React Frontend
                      │
                      ▼
                Backend API
                      │
                      ▼
             User Query Processing
                      │
                      ▼
              Vector Retrieval
                      │
                      ▼
                 ChromaDB
                      │
             Relevant Documents
                      │
                      ▼
              RAG Prompt Builder
                      │
                      ▼
                 Groq LLM
                      │
                      ▼
             Generated Response
                      │
                      ▼
              React Chat Interface
```

## RAG Workflow

1. VJIT information is collected and stored in the project knowledge base.
2. Documents are processed and converted into vector embeddings.
3. The embeddings are stored in ChromaDB.
4. When a user asks a question, semantic search retrieves the most relevant chunks.
5. The retrieved information is added to the LLM prompt as context.
6. The Groq-hosted LLM generates an answer based on the retrieved information.
7. The response is streamed back to the frontend and displayed to the user.

## Tech Stack

| Layer               | Technology            |
| ------------------- | --------------------- |
| Frontend            | React, Vite, CSS      |
| Backend             | Python                |
| LLM                 | Groq API              |
| Vector Database     | ChromaDB              |
| Embeddings          | Sentence Transformers |
| Response Formatting | React Markdown        |
| Version Control     | Git, GitHub           |

## Project Structure

```text
college-enquiry-chatbot/
│
├── backend/
│   ├── data/
│   │   └── fees_structure.txt.txt
│   ├── rag_chain.py
│   ├── chroma_utils.py
│   └── ...
│
├── frontend/
│   ├── public/
│   │   └── vjit-logo.png
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── style.css
│   ├── package.json
│   └── package-lock.json
│
├── .gitignore
└── README.md
```

## Example Queries

The chatbot can answer questions such as:

```text
What courses are offered at VJIT?

What is the fee structure?

Why should I choose VJIT?

What are the placement opportunities?

What facilities are available?

Where is VJIT located?

Which companies recruit from VJIT?
```

## Response Design

The chatbot is designed to provide:

* Direct answers to user queries
* Short and relevant responses
* Easy-to-understand language
* Markdown formatting for readability
* Context-grounded responses
* Fallback responses when relevant information is unavailable

## Getting Started

### Prerequisites

Make sure the following are installed:

* Python 3.x
* Node.js and npm
* Git
* A Groq API key

### Clone the Repository

```bash
git clone https://github.com/Srinivas2299/college-enquiry-chatbot.git
cd college-enquiry-chatbot
```

### Backend Setup

```bash
cd backend
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file inside the backend directory:

```env
GROQ_API_KEY=your_groq_api_key
```

Start the backend using the project's configured entry point.

### Frontend Setup

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL provided by Vite in your browser.

## Environment Variables

The application requires a Groq API key:

```env
GROQ_API_KEY=your_groq_api_key
```

The `.env` file should **not** be committed to GitHub.

## Future Improvements

* Expand the knowledge base with additional VJIT documents
* Improve retrieval accuracy through better chunking and metadata
* Add source references to chatbot responses
* Add conversation history and context-aware follow-up questions
* Add automated evaluation for retrieval and answer quality
* Deploy the application for public access
* Add an admin interface for updating the knowledge base

## Project Status

The core RAG pipeline and chatbot interface are implemented.

Current development focus includes improving retrieval accuracy, testing edge cases, and preparing the application for deployment.

## Author

**Reddysetty Srinivas**

GitHub: https://github.com/Srinivas2299/college-enquiry-chatbot

## Disclaimer

This project is developed as an academic project for demonstrating the use of **Retrieval-Augmented Generation, vector search, and LLM-based conversational applications**.

The accuracy of responses depends on the information available in the project's knowledge base.
