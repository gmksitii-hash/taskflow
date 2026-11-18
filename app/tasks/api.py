from datetime import date
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from app.tasks.domain import Task, TaskService, TaskStatus, TaskValidationError

router = APIRouter(prefix="/tasks", tags=["Tasks"])
task_service = TaskService()


class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    due_date: date | None = None
    assignee: str | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    status: TaskStatus
    assignee: str | None
    due_date: date | None


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task_endpoint(payload: TaskCreateRequest) -> Task:
    try:
        return task_service.create_task(
            title=payload.title,
            due_date=payload.due_date,
            assignee=payload.assignee,
        )
    except TaskValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.get("", response_model=list[TaskResponse])
def get_tasks_endpoint() -> list[Task]:
    return task_service.list_tasks()
