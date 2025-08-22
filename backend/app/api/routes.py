from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.schemas.interview import InterviewGenerationRequest, InterviewResponse
from app.services.interview_generator import interview_generator
from typing import Dict
import uuid
from datetime import datetime
import asyncio

router = APIRouter()

# In-memory storage for demo (replace with database in production)
interviews_storage: Dict[str, InterviewResponse] = {}

@router.post("/generate-interview", response_model=InterviewResponse)
async def generate_interview(
    request: InterviewGenerationRequest,
    background_tasks: BackgroundTasks
):
    """Generate a new interview transcript based on the request."""
    
    # Create interview ID
    interview_id = str(uuid.uuid4())
    
    # Initialize response with generating status
    response = InterviewResponse(
        interview_id=interview_id,
        status="generating",
        interview=None
    )
    
    # Store initial response
    interviews_storage[interview_id] = response
    
    # Start background generation
    background_tasks.add_task(generate_interview_background, interview_id, request)
    
    return response

@router.get("/interviews/{interview_id}", response_model=InterviewResponse)
async def get_interview(interview_id: str):
    """Get an interview by ID."""
    
    if interview_id not in interviews_storage:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    return interviews_storage[interview_id]

@router.get("/interviews")
async def list_interviews():
    """List all generated interviews."""
    
    return {
        "interviews": [
            {
                "interview_id": interview_id,
                "status": response.status,
                "topic": response.interview.topic if response.interview else None,
                "generated_at": response.generated_at
            }
            for interview_id, response in interviews_storage.items()
        ]
    }

@router.delete("/interviews/{interview_id}")
async def delete_interview(interview_id: str):
    """Delete an interview."""
    
    if interview_id not in interviews_storage:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    del interviews_storage[interview_id]
    return {"message": "Interview deleted successfully"}

async def generate_interview_background(interview_id: str, request: InterviewGenerationRequest):
    """Background task to generate interview transcript."""
    
    try:
        # Generate the interview
        interview_transcript = await interview_generator.generate_interview(request)
        
        # Update storage with completed interview
        interviews_storage[interview_id] = InterviewResponse(
            interview_id=interview_id,
            status="completed",
            interview=interview_transcript,
            generated_at=datetime.now().isoformat()
        )
        
    except Exception as e:
        # Update storage with error
        interviews_storage[interview_id] = InterviewResponse(
            interview_id=interview_id,
            status="failed",
            interview=None,
            error_message=str(e),
            generated_at=datetime.now().isoformat()
        )
