# 🧠 SmartNotes

<p align="center">
  <img src="frontend/src/assets/logo.png" width="120" alt="SmartNotes Logo"/>
</p>

<h3 align="center">
AI-Powered Note Taking, Summarization & RAG Chat Assistant
</h3>

<p align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![MongoDB](https://img.shields.io/badge/MongoDB-4DB33D?style=for-the-badge&logo=mongodb&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-000000?style=for-the-badge)
![FAISS](https://img.shields.io/badge/FAISS-4285F4?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-000000?style=for-the-badge)
![Llama 3.3](https://img.shields.io/badge/Llama_3.3_70B-FF6B35?style=for-the-badge)
![Firebase](https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase)

</p>

---

# 📖 Overview

**SmartNotes** is an AI-powered note-taking and content summarization platform that leverages **Retrieval-Augmented Generation (RAG)** to transform lengthy content into concise, meaningful summaries while allowing users to interact intelligently with their notes.

The platform enables users to summarize content from multiple sources including **YouTube videos, PDF documents, audio files, and videos**, then ask AI-powered questions, generate flashcards, and manage their learning materials from one centralized dashboard.

---

# ✨ Features

## 📹 YouTube Video Summarization

- Extracts YouTube transcripts
- AI-generated structured summaries
- Video preview
- Transcript viewer
- Copy transcript
- Save summaries
- Export summary to PDF

---

## 📄 PDF Summarization

- Upload PDF documents
- Automatic text extraction
- Intelligent summarization
- Save notes
- AI-powered chat
- Flashcard generation

---

## 🎙 Audio & Video Summarization

Supports media uploads using **Faster Whisper**.

Features include:

- Audio transcription
- Video transcription
- AI summaries
- Save notes
- Interactive AI chat

---

## 🤖 AI Chat Assistant (RAG)

Instead of simply chatting with an LLM, SmartNotes uses **Retrieval-Augmented Generation (RAG)**.

Users can:

- Ask questions about uploaded content
- Receive context-aware answers
- Continue conversations
- Generate intelligent follow-up prompts

---

## 📚 Flashcard Generator

Convert summaries into study material instantly.

- Question & Answer format
- Exam preparation
- Revision notes
- AI-generated flashcards

---

## 🕒 History Management

All summaries are automatically saved.

Features include:

- Search previous notes
- View history
- Delete notes
- Persistent storage in MongoDB

---

## 🔐 Authentication

Firebase Authentication provides:

- Secure Login
- User Registration
- Session Management
- Protected Routes

---

## 📄 PDF Export

Users can:

- Download summaries
- Copy summaries
- Store notes permanently

---

# 🧠 AI Stack

| Component | Technology |
|-----------|------------|
| LLM | Llama 3.3 70B (Groq) |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Vector Store | FAISS |
| Framework | LangChain |
| Speech-to-Text | Faster Whisper |
| Database | MongoDB |

---

# 🏗 Tech Stack

## Frontend

- React 19
- Vite
- Tailwind CSS
- React Router
- Firebase Authentication
- React Markdown
- Lucide Icons
- jsPDF
- Framer Motion

---

## Backend

- FastAPI
- MongoDB
- LangChain
- FAISS
- Faster Whisper
- HuggingFace Embeddings
- Groq API
- Uvicorn

---

# 📂 Project Structure

```
SmartNotes
│
├── backend
│   ├── database
│   │   ├── config.py
│   │   ├── crud.py
│   │   └── historySchema.py
│   │
│   ├── services
│   │   ├── media_summariser
│   │   │   ├── embed.py
│   │   │   └── process_media.py
│   │   │
│   │   ├── Media_summarizer.py
│   │   ├── PDF_summarizer.py
│   │   └── YT_summarizer.py
│   │
│   ├── utils
│   │   ├── pdf_loader.py
│   │   └── youtube_transcript.py
│   │
│   ├── main.py
│   └── requirements.txt
│
├── frontend
│   ├── src
│   │   ├── components
│   │   ├── pages
│   │   ├── context
│   │   └── assets
│   │
│   └── package.json
│
└── README.md
```

---

# ⚙️ Architecture

```text
                    User
                      │
                      ▼
             React Frontend
                      │
          REST API Requests
                      │
                      ▼
              FastAPI Backend
      ┌─────────┬──────────┬─────────┐
      │         │          │
      ▼         ▼          ▼
 PDF Service  Media Service  YouTube Service
      │         │          │
      └─────────┴──────────┘
                │
        Text Extraction
                │
                ▼
         Chunk Documents
                │
                ▼
 HuggingFace Embeddings
(all-MiniLM-L6-v2)
                │
                ▼
            FAISS Index
                │
                ▼
          Llama 3.3 70B
             (Groq API)
                │
                ▼
      Summary / Chat / Flashcards
                │
                ▼
             MongoDB
```

---

# 🔄 RAG Workflow

```text
User Uploads Content
        │
        ▼
Extract Text / Transcript
        │
        ▼
Chunk Documents
        │
        ▼
Generate Embeddings
        │
        ▼
Store in FAISS
        │
        ▼
Generate AI Summary
        │
        ▼
Save Summary to MongoDB
        │
        ▼
User asks Question
        │
        ▼
Retrieve Relevant Chunks
        │
        ▼
Send Context + Prompt
        │
        ▼
Llama 3.3 70B (Groq)
        │
        ▼
Context-Aware Answer
```

---

# 📡 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/transcript/` | Get YouTube Transcript |
| POST | `/summarize-yt` | Summarize YouTube Video |
| POST | `/summarize-pdf` | Summarize PDF |
| POST | `/summarize-media` | Summarize Audio / Video |
| GET | `/notes/` | Get User Notes |
| DELETE | `/notes/{note_id}` | Delete Note |
| POST | `/summarize-flashcard` | Generate Flashcards |
| POST | `/prompts` | Generate Suggested Prompts |
| POST | `/chat` | Chat using RAG |


---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/Vedant8075/SmartNotes.git
```

```
cd SmartNotes
```

---

# Backend Setup

```bash
cd backend
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run server

```bash
uvicorn main:app --reload
```

---

# Frontend Setup

```bash
cd frontend
```

Install dependencies

```bash
npm install
```

Run

```bash
npm run dev
```

---

# 🔑 Environment Variables

Create a `.env` file inside the backend.

```env
GROQ_API_KEY=

MONGODB_URI=

HF_TOKEN=

FIREBASE_API_KEY=

FIREBASE_AUTH_DOMAIN=

FIREBASE_PROJECT_ID=

FIREBASE_STORAGE_BUCKET=

FIREBASE_MESSAGING_SENDER_ID=

FIREBASE_APP_ID=
```

---

# 💡 Why SmartNotes?

SmartNotes was built to solve the growing challenge of **information overload**. Instead of manually reading lengthy documents or watching long videos, users can quickly generate concise summaries, ask contextual questions using AI, and create flashcards for effective revision.

By combining **LLMs**, **semantic search**, and **Retrieval-Augmented Generation (RAG)**, SmartNotes transforms passive content into an interactive learning experience.

---

# 🚀 Future Improvements

- Image OCR summarization
- Multi-language support
- Shared workspaces
- AI note organization
- Voice-based AI chat
- Real-time streaming responses
- Cloud deployment
- Mobile application
- AI-generated quizzes
- Note sharing

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository

2. Create your feature branch

```bash
git checkout -b feature-name
```

3. Commit changes

```bash
git commit -m "Added new feature"
```

4. Push

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Vedant Gupta**

If you found this project helpful, consider giving it a ⭐ on GitHub!

---

<h3 align="center">
Built with ❤️ using FastAPI, React, LangChain, FAISS & Llama 3.3
</h3>
