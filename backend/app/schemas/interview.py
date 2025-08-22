from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class InterviewTopic(str, Enum):
    SOFTWARE_ENGINEERING = "Software Engineering"
    PRODUCT_MANAGEMENT = "Product Management"
    DATA_SCIENCE = "Data Science"
    FRONTEND_ENGINEERING = "Frontend Engineering"
    BACKEND_ENGINEERING = "Backend Engineering"
    DEVOPS_ENGINEERING = "DevOps Engineering"
    MOBILE_DEVELOPMENT = "Mobile Development"
    MACHINE_LEARNING = "Machine Learning"

class DifficultyLevel(str, Enum):
    JUNIOR = "junior"
    MID_LEVEL = "mid-level"
    SENIOR = "senior"
    STAFF = "staff"

class CompanyType(str, Enum):
    STARTUP = "startup"
    BIG_TECH = "big-tech"
    ENTERPRISE = "enterprise"
    CONSULTING = "consulting"

class InterviewGenerationRequest(BaseModel):
    topic: InterviewTopic
    difficulty: DifficultyLevel = DifficultyLevel.MID_LEVEL
    duration_minutes: int = Field(default=45, ge=15, le=120, description="Interview duration in minutes")
    company_type: CompanyType = CompanyType.STARTUP
    focus_areas: List[str] = Field(default=["technical", "behavioral"], description="Areas to focus on")
    interviewer_name: Optional[str] = None
    interviewee_name: Optional[str] = None

class Exchange(BaseModel):
    speaker: str  # "interviewer" or "interviewee"
    text: str
    timestamp: str  # Format: "MM:SS"

class Chapter(BaseModel):
    title: str
    duration_minutes: int
    description: str
    exchanges: List[Exchange]

class Participant(BaseModel):
    name: str
    role: str
    company: Optional[str] = None

class InterviewTranscript(BaseModel):
    topic: str
    difficulty: str
    total_duration_minutes: int
    participants: Dict[str, Participant]
    chapters: List[Chapter]
    metadata: Dict[str, Any] = {}

class InterviewResponse(BaseModel):
    interview_id: str
    status: str  # "generating", "completed", "failed"
    interview: Optional[InterviewTranscript] = None
    error_message: Optional[str] = None
    generated_at: Optional[str] = None
