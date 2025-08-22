# Vibecode - YouTube Interview Transcript Parser

A full-stack application that processes YouTube interview transcripts and parses them into structured data including summaries, highlights, and executable tasks.

## Architecture

- **Backend**: FastAPI (Python)
- **Frontend**: Next.js with Tailwind CSS
- **Database**: Supabase (PostgreSQL)
- **AI Processing**: OpenAI API

## Project Structure

```
Vibecode/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── main.py         # FastAPI app
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # App router pages
│   │   ├── components/    # React components
│   │   ├── lib/          # Utilities
│   │   └── types/        # TypeScript types
│   ├── package.json
│   └── tailwind.config.js
├── database/              # Database schemas and migrations
└── docker-compose.yml     # Local development setup
```

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (optional)

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Environment Variables
Copy `.env.example` to `.env` and fill in your configuration.

## Features

- 📤 Upload YouTube transcript JSON files
- 🤖 AI-powered parsing into structured content
- 📋 Extract executable tasks and action items
- 📊 Generate intro summaries and highlights
- ✅ Task management and tracking
- 🔍 Search and filter interviews
- 📱 Responsive modern UI

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.
