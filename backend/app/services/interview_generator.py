from openai import OpenAI
from app.core.config import settings
from app.schemas.interview import InterviewGenerationRequest, InterviewTranscript, Chapter, Exchange, Participant
from typing import Dict, Any, List
import json
import uuid
import random

class InterviewGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    async def generate_interview(self, request: InterviewGenerationRequest) -> InterviewTranscript:
        """Generate a complete interview transcript based on the request."""
        
        # Generate participant names if not provided
        interviewer_name = request.interviewer_name or self._generate_interviewer_name()
        interviewee_name = request.interviewee_name or self._generate_interviewee_name()
        
        # Create the system prompt
        system_prompt = self._create_system_prompt(request, interviewer_name, interviewee_name)
        
        # Generate the interview content
        user_prompt = self._create_user_prompt(request)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content
            interview_data = json.loads(content)
            
            # Convert to our schema
            return self._convert_to_transcript(interview_data, request, interviewer_name, interviewee_name)
            
        except Exception as e:
            raise Exception(f"Error generating interview with OpenAI: {str(e)}")

    def _create_system_prompt(self, request: InterviewGenerationRequest, interviewer_name: str, interviewee_name: str) -> str:
        """Create the system prompt for interview generation."""
        return f"""You are an expert at creating realistic technical interview transcripts. 

Generate a {request.topic.value} interview between:
- Interviewer: {interviewer_name} (Senior hiring manager at a {request.company_type.value} company)
- Interviewee: {interviewee_name} ({request.difficulty.value} level candidate)

Requirements:
- Duration: {request.duration_minutes} minutes total
- Difficulty: {request.difficulty.value}
- Company type: {request.company_type.value}
- Focus areas: {', '.join(request.focus_areas)}

Create a realistic back-and-forth conversation with:
1. Natural dialogue and realistic responses
2. Technical questions appropriate for the level
3. Follow-up questions based on answers
4. Realistic pauses, clarifications, and thinking moments
5. Structured chapters covering different topics

Return ONLY valid JSON in this exact format:
{{
  "chapters": [
    {{
      "title": "Introduction & Background",
      "duration_minutes": 5,
      "description": "Getting to know the candidate",
      "exchanges": [
        {{
          "speaker": "interviewer",
          "text": "Hi {interviewee_name}, thanks for joining us today...",
          "timestamp": "00:00"
        }},
        {{
          "speaker": "interviewee", 
          "text": "Thank you for having me, {interviewer_name}...",
          "timestamp": "00:15"
        }}
      ]
    }}
  ]
}}

Make it feel authentic with realistic technical discussions, problem-solving, and natural conversation flow."""

    def _create_user_prompt(self, request: InterviewGenerationRequest) -> str:
        """Create the user prompt with specific requirements."""
        
        # Define chapter structure based on topic
        chapter_suggestions = self._get_chapter_suggestions(request.topic, request.duration_minutes)
        
        return f"""Generate a {request.duration_minutes}-minute {request.topic.value} interview with these chapters:

{chapter_suggestions}

Make sure to:
- Include realistic technical questions for {request.difficulty.value} level
- Show natural conversation flow with follow-ups
- Include moments where candidate asks clarifying questions
- Add realistic thinking pauses and "umm" moments
- Make the interviewer ask progressively harder questions
- Include both technical and behavioral elements
- End with candidate questions for the interviewer

Generate the complete JSON structure now."""

    def _get_chapter_suggestions(self, topic, duration_minutes: int) -> str:
        """Get suggested chapters based on interview topic and duration."""
        
        base_chapters = {
            "Software Engineering": [
                "Introduction & Background (5 min)",
                "Technical Experience Discussion (10 min)", 
                "Coding Problem - Easy (10 min)",
                "Coding Problem - Medium (15 min)",
                "System Design Discussion (10 min)",
                "Behavioral Questions (8 min)",
                "Questions for Interviewer (2 min)"
            ],
            "Frontend Engineering": [
                "Introduction & Background (5 min)",
                "Frontend Technologies Discussion (8 min)",
                "JavaScript/React Coding (15 min)", 
                "CSS & Responsive Design (10 min)",
                "Performance Optimization (7 min)",
                "Behavioral Questions (5 min)",
                "Questions for Interviewer (3 min)"
            ],
            "Product Management": [
                "Introduction & Background (5 min)",
                "Product Strategy Discussion (12 min)",
                "Case Study - Feature Design (15 min)",
                "Metrics & Analytics (8 min)",
                "Stakeholder Management (10 min)",
                "Behavioral Questions (8 min)",
                "Questions for Interviewer (2 min)"
            ]
        }
        
        chapters = base_chapters.get(topic.value, base_chapters["Software Engineering"])
        return "\n".join([f"- {chapter}" for chapter in chapters])

    def _convert_to_transcript(self, interview_data: Dict[str, Any], request: InterviewGenerationRequest, 
                             interviewer_name: str, interviewee_name: str) -> InterviewTranscript:
        """Convert the AI response to our InterviewTranscript schema."""
        
        chapters = []
        for chapter_data in interview_data.get("chapters", []):
            exchanges = []
            for exchange_data in chapter_data.get("exchanges", []):
                exchanges.append(Exchange(
                    speaker=exchange_data["speaker"],
                    text=exchange_data["text"],
                    timestamp=exchange_data["timestamp"]
                ))
            
            chapters.append(Chapter(
                title=chapter_data["title"],
                duration_minutes=chapter_data["duration_minutes"],
                description=chapter_data.get("description", ""),
                exchanges=exchanges
            ))
        
        participants = {
            "interviewer": Participant(
                name=interviewer_name,
                role="Senior Hiring Manager",
                company=f"{request.company_type.value.title()} Company"
            ),
            "interviewee": Participant(
                name=interviewee_name,
                role=f"{request.difficulty.value.title()} {request.topic.value}",
                company=None
            )
        }
        
        return InterviewTranscript(
            topic=request.topic.value,
            difficulty=request.difficulty.value,
            total_duration_minutes=request.duration_minutes,
            participants=participants,
            chapters=chapters,
            metadata={
                "company_type": request.company_type.value,
                "focus_areas": request.focus_areas,
                "generated_with": settings.OPENAI_MODEL
            }
        )

    def _generate_interviewer_name(self) -> str:
        """Generate a random interviewer name."""
        first_names = ["Sarah", "Michael", "Jennifer", "David", "Lisa", "James", "Emily", "Robert", "Maria", "Kevin"]
        last_names = ["Chen", "Johnson", "Williams", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson"]
        return f"{random.choice(first_names)} {random.choice(last_names)}"

    def _generate_interviewee_name(self) -> str:
        """Generate a random interviewee name."""
        first_names = ["Alex", "Jordan", "Taylor", "Casey", "Morgan", "Riley", "Avery", "Quinn", "Cameron", "Drew"]
        last_names = ["Rodriguez", "Kim", "Patel", "Thompson", "Garcia", "Martinez", "Lee", "White", "Harris", "Clark"]
        return f"{random.choice(first_names)} {random.choice(last_names)}"

interview_generator = InterviewGenerator()
