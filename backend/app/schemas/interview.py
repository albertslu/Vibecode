from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class InterviewStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class InterviewCreate(BaseModel):
    title: str
    youtube_url: Optional[str] = None
    raw_transcript: str = Field(..., min_length=50, description="Plain text transcript content")

class InterviewResponse(BaseModel):
    id: str
    title: str
    youtube_url: Optional[str]
    status: InterviewStatus
    processed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    # Parsed content (if available)
    intro_summary: Optional[str] = None
    highlights: Optional[Dict[Any, Any]] = None
    lowlights: Optional[Dict[Any, Any]] = None
    key_entities: Optional[Dict[Any, Any]] = None

class InterviewList(BaseModel):
    id: str
    title: str
    status: InterviewStatus
    created_at: datetime
    processed_at: Optional[datetime]

class ParsedContent(BaseModel):
    intro_summary: str
    highlights: Dict[Any, Any]
    lowlights: Dict[Any, Any]
    key_entities: Dict[Any, Any]
