# Vibecode - AI Interview Transcript Generator

An AI-powered application that generates realistic interview transcripts based on topics like Software Engineering, Product Management, Data Science, etc. Creates structured, chapter-based conversations between interviewer and interviewee.

## Architecture

- **Backend**: FastAPI (Python)
- **Frontend**: Next.js with Tailwind CSS
- **AI Generation**: OpenAI GPT-4o Mini
- **Storage**: Local file system / Optional cloud storage

## Project Structure

```
Vibecode/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configuration
│   │   ├── services/       # AI generation logic
│   │   ├── schemas/        # Data models
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
└── docker-compose.yml     # Local development setup
```

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- OpenAI API Key

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
Copy `env.template` to `.env` and add your OpenAI API key.

## Features

- 🎯 **Topic-based Generation**: Software Engineering, PM, Data Science interviews
- 💬 **Realistic Dialogue**: Natural back-and-forth conversations
- 📚 **Structured Chapters**: Frontend, Backend, System Design, Behavioral sections
- ⚙️ **Customizable**: Interview length, difficulty, company type
- 📄 **Multiple Formats**: JSON, plain text, formatted transcripts
- 🎨 **Modern UI**: Clean, responsive interface

## Sample Output

```json
{
  "interview": {
    "topic": "Software Engineering Interview",
    "participants": {
      "interviewer": "Sarah Chen, Senior Engineering Manager",
      "interviewee": "Alex Rodriguez, Software Engineer"
    },
    "chapters": [
      {
        "title": "Frontend Development",
        "duration": "15 minutes",
        "exchanges": [
          {
            "speaker": "interviewer",
            "text": "Can you walk me through how you'd optimize a React application?",
            "timestamp": "05:30"
          }
        ]
      }
    ]
  }
}
```

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.
