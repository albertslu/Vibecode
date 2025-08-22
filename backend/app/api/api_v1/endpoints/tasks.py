from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import TaskService

router = APIRouter()

@router.get("/", response_model=List[TaskResponse])
async def list_tasks(
    interview_id: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    """Get list of tasks with optional filtering."""
    # TODO: Implement task service
    # tasks = await TaskService.get_tasks(
    #     interview_id=interview_id,
    #     status=status,
    #     skip=skip,
    #     limit=limit
    # )
    # return tasks
    
    return []

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """Get a specific task by ID."""
    # TODO: Implement task service
    # task = await TaskService.get_task(task_id)
    # if not task:
    #     raise HTTPException(status_code=404, detail="Task not found")
    # return task
    
    return {"message": f"Get task {task_id} - implementation pending"}

@router.post("/", response_model=TaskResponse)
async def create_task(task_data: TaskCreate, interview_id: str):
    """Create a new task for an interview."""
    # TODO: Implement task service
    # task = await TaskService.create_task(task_data, interview_id)
    # return task
    
    return {"message": "Create task - implementation pending"}

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, task_data: TaskUpdate):
    """Update an existing task."""
    # TODO: Implement task service
    # task = await TaskService.update_task(task_id, task_data)
    # if not task:
    #     raise HTTPException(status_code=404, detail="Task not found")
    # return task
    
    return {"message": f"Update task {task_id} - implementation pending"}

@router.delete("/{task_id}")
async def delete_task(task_id: str):
    """Delete a task."""
    # TODO: Implement task service
    # await TaskService.delete_task(task_id)
    
    return {"message": f"Delete task {task_id} - implementation pending"}
