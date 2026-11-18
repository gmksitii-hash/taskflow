from dataclasses import dataclass
from datetime import date
from enum import Enum


class TaskStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"


@dataclass
class Task:
    id: int
    title: str
    status: TaskStatus = TaskStatus.NEW
    assignee: str | None = None
    due_date: date | None = None


class TaskValidationError(ValueError):
    """Помилка валідації бізнес-правил завдання."""


class TaskService:
    def __init__(self) -> None:
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def create_task(
        self,
        title: str,
        due_date: date | None = None,
        assignee: str | None = None,
    ) -> Task:
        clean_title = title.strip()
        if not clean_title:
            raise TaskValidationError("Назва завдання не може бути порожньою.")
        if due_date is not None and due_date < date.today():
            raise TaskValidationError("Термін виконання не може бути в минулому.")

        task = Task(
            id=self._next_id,
            title=clean_title,
            assignee=assignee,
            due_date=due_date,
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def list_tasks(self) -> list[Task]:
        return list(self._tasks)




    def update_status(self, task_id: int, new_status: TaskStatus) -> Task:
        for task in self._tasks:
            if task.id == task_id:
                task.status = new_status
                return task
        raise TaskValidationError(f"Завдання з ID {task_id} не знайдено.")
