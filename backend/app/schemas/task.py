from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    category: Optional[str] = None
    due_date: Optional[date] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    category: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[TaskStatus] = None

class TaskResponse(BaseModel):
    id: str
    interview_id: str
    user_id: str
    title: str
    description: Optional[str]
    priority: TaskPriority
    category: Optional[str]
    due_date: Optional[date]
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
