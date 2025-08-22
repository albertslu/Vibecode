from app.core.database import supabase_client
from app.schemas.interview import InterviewCreate, InterviewResponse, InterviewList
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

class SupabaseService:
    def __init__(self):
        self.client = supabase_client

    # Interview operations
    async def create_interview(self, interview_data: InterviewCreate, user_id: str) -> Dict[str, Any]:
        """Create a new interview record in Supabase."""
        try:
            result = self.client.table("interviews").insert({
                "user_id": user_id,
                "title": interview_data.title,
                "youtube_url": interview_data.youtube_url,
                "raw_transcript": interview_data.raw_transcript,
                "status": "pending"
            }).execute()
            
            if result.data:
                return result.data[0]
            else:
                raise Exception("Failed to create interview")
                
        except Exception as e:
            raise Exception(f"Database error creating interview: {str(e)}")

    async def get_interview(self, interview_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get interview by ID with parsed content."""
        try:
            # Get interview with parsed content
            result = self.client.table("interviews").select(
                "*, parsed_content(*)"
            ).eq("id", interview_id).eq("user_id", user_id).execute()
            
            if result.data:
                interview = result.data[0]
                # Flatten parsed content if it exists
                if interview.get("parsed_content"):
                    parsed = interview["parsed_content"][0] if interview["parsed_content"] else {}
                    interview.update({
                        "intro_summary": parsed.get("intro_summary"),
                        "highlights": parsed.get("highlights"),
                        "lowlights": parsed.get("lowlights"),
                        "key_entities": parsed.get("key_entities")
                    })
                return interview
            return None
            
        except Exception as e:
            raise Exception(f"Database error getting interview: {str(e)}")

    async def get_interviews(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get list of user's interviews."""
        try:
            result = self.client.table("interviews").select(
                "id, title, status, created_at, processed_at"
            ).eq("user_id", user_id).order("created_at", desc=True).range(skip, skip + limit - 1).execute()
            
            return result.data or []
            
        except Exception as e:
            raise Exception(f"Database error getting interviews: {str(e)}")

    async def update_interview_status(self, interview_id: str, status: str, processed_at: Optional[datetime] = None) -> bool:
        """Update interview processing status."""
        try:
            update_data = {"status": status}
            if processed_at:
                update_data["processed_at"] = processed_at.isoformat()
                
            result = self.client.table("interviews").update(update_data).eq("id", interview_id).execute()
            return len(result.data) > 0
            
        except Exception as e:
            raise Exception(f"Database error updating interview status: {str(e)}")

    async def save_parsed_content(self, interview_id: str, parsed_data: Dict[str, Any]) -> bool:
        """Save parsed content to database."""
        try:
            # First, delete existing parsed content
            self.client.table("parsed_content").delete().eq("interview_id", interview_id).execute()
            
            # Insert new parsed content
            result = self.client.table("parsed_content").insert({
                "interview_id": interview_id,
                "intro_summary": parsed_data.get("intro_summary"),
                "highlights": parsed_data.get("highlights"),
                "lowlights": parsed_data.get("lowlights"),
                "key_entities": parsed_data.get("key_entities")
            }).execute()
            
            return len(result.data) > 0
            
        except Exception as e:
            raise Exception(f"Database error saving parsed content: {str(e)}")

    async def delete_interview(self, interview_id: str, user_id: str) -> bool:
        """Delete interview and all related data."""
        try:
            result = self.client.table("interviews").delete().eq("id", interview_id).eq("user_id", user_id).execute()
            return len(result.data) > 0
            
        except Exception as e:
            raise Exception(f"Database error deleting interview: {str(e)}")

    # Task operations
    async def create_task(self, task_data: TaskCreate, interview_id: str, user_id: str) -> Dict[str, Any]:
        """Create a new task."""
        try:
            result = self.client.table("tasks").insert({
                "interview_id": interview_id,
                "user_id": user_id,
                "title": task_data.title,
                "description": task_data.description,
                "priority": task_data.priority,
                "category": task_data.category,
                "due_date": task_data.due_date.isoformat() if task_data.due_date else None,
                "status": "pending"
            }).execute()
            
            if result.data:
                return result.data[0]
            else:
                raise Exception("Failed to create task")
                
        except Exception as e:
            raise Exception(f"Database error creating task: {str(e)}")

    async def get_tasks(self, user_id: str, interview_id: Optional[str] = None, status: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get tasks with optional filtering."""
        try:
            query = self.client.table("tasks").select("*").eq("user_id", user_id)
            
            if interview_id:
                query = query.eq("interview_id", interview_id)
            if status:
                query = query.eq("status", status)
                
            result = query.order("created_at", desc=True).range(skip, skip + limit - 1).execute()
            return result.data or []
            
        except Exception as e:
            raise Exception(f"Database error getting tasks: {str(e)}")

    async def get_task(self, task_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get task by ID."""
        try:
            result = self.client.table("tasks").select("*").eq("id", task_id).eq("user_id", user_id).execute()
            return result.data[0] if result.data else None
            
        except Exception as e:
            raise Exception(f"Database error getting task: {str(e)}")

    async def update_task(self, task_id: str, task_data: TaskUpdate, user_id: str) -> Optional[Dict[str, Any]]:
        """Update an existing task."""
        try:
            update_data = {}
            if task_data.title is not None:
                update_data["title"] = task_data.title
            if task_data.description is not None:
                update_data["description"] = task_data.description
            if task_data.priority is not None:
                update_data["priority"] = task_data.priority
            if task_data.category is not None:
                update_data["category"] = task_data.category
            if task_data.due_date is not None:
                update_data["due_date"] = task_data.due_date.isoformat() if task_data.due_date else None
            if task_data.status is not None:
                update_data["status"] = task_data.status
                
            result = self.client.table("tasks").update(update_data).eq("id", task_id).eq("user_id", user_id).execute()
            return result.data[0] if result.data else None
            
        except Exception as e:
            raise Exception(f"Database error updating task: {str(e)}")

    async def delete_task(self, task_id: str, user_id: str) -> bool:
        """Delete a task."""
        try:
            result = self.client.table("tasks").delete().eq("id", task_id).eq("user_id", user_id).execute()
            return len(result.data) > 0
            
        except Exception as e:
            raise Exception(f"Database error deleting task: {str(e)}")

    async def create_tasks_from_parsed_data(self, interview_id: str, user_id: str, executable_tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create multiple tasks from parsed transcript data."""
        try:
            tasks_to_insert = []
            for task_data in executable_tasks:
                tasks_to_insert.append({
                    "interview_id": interview_id,
                    "user_id": user_id,
                    "title": task_data.get("title", "Untitled Task"),
                    "description": task_data.get("description", ""),
                    "priority": task_data.get("priority", "medium"),
                    "category": task_data.get("category", "general"),
                    "status": "pending"
                })
            
            if tasks_to_insert:
                result = self.client.table("tasks").insert(tasks_to_insert).execute()
                return result.data or []
            return []
            
        except Exception as e:
            raise Exception(f"Database error creating tasks from parsed data: {str(e)}")

supabase_service = SupabaseService()
