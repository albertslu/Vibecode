from openai import OpenAI
from app.core.config import settings
from typing import Dict, Any
import json

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    async def parse_transcript(self, transcript_text: str) -> Dict[str, Any]:
        """
        Parse YouTube transcript (plain text) using GPT-4o Mini to extract:
        - Intro summary
        - Highlights
        - Lowlights  
        - Key entities
        - Executable tasks
        """
        
        # Validate input
        if not transcript_text or len(transcript_text.strip()) < 50:
            raise ValueError("Transcript text is too short or empty")
        
        system_prompt = """You are an expert at analyzing interview transcripts. 
        Parse the following YouTube interview transcript and extract:

        1. INTRO_SUMMARY: A 2-3 sentence overview of the interview, participants, and main topic
        2. HIGHLIGHTS: Key positive moments, insights, or achievements mentioned (as array of objects with timestamp and description)
        3. LOWLIGHTS: Challenges, failures, or difficult moments discussed (as array of objects with timestamp and description)  
        4. KEY_ENTITIES: Important people, companies, technologies, or concepts mentioned (as object with categories)
        5. EXECUTABLE_TASKS: Specific action items, follow-ups, or takeaways that could be tracked (as array of task objects)

        Return the response as valid JSON with these exact keys: intro_summary, highlights, lowlights, key_entities, executable_tasks.
        
        For tasks, include: title, description, priority (low/medium/high), category, and estimated_due_days.
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Transcript to analyze:\n\n{transcript_text}"}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            parsed_data = json.loads(content)
            
            return parsed_data
            
        except Exception as e:
            raise Exception(f"Error parsing transcript with OpenAI: {str(e)}")

    def _clean_transcript_text(self, text: str) -> str:
        """Clean and prepare transcript text for processing."""
        # Remove excessive whitespace and normalize
        cleaned = " ".join(text.split())
        
        # Truncate if too long (GPT-4o-mini has token limits)
        max_chars = 12000  # Roughly 3000 tokens
        if len(cleaned) > max_chars:
            cleaned = cleaned[:max_chars] + "..."
            
        return cleaned

openai_service = OpenAIService()
