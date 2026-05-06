from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models.task import Task, TaskPriority, TaskStatus
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_or_404(task_public_id: UUID, db: Session, current_user: User) -> Task:
    task = (
        db.query(Task)
        .filter(
            Task.public_id == str(task_public_id),
            Task.owner_id == current_user.id,
            Task.is_deleted == False,  # noqa: E712
        )
        .first()
    )
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    status_filter: TaskStatus | None = Query(default=None, alias="status"),
    priority_filter: TaskPriority | None = Query(default=None, alias="priority"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Task).filter(
        Task.owner_id == current_user.id,
        Task.is_deleted == False,  # noqa: E712
    )
    if status_filter is not None:
        query = query.filter(Task.status == status_filter)
    if priority_filter is not None:
        query = query.filter(Task.priority == priority_filter)
    tasks = query.order_by(Task.created_at.desc()).all()
    return [TaskResponse.model_validate(t) for t in tasks]


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = Task(**task_in.model_dump(), owner_id=current_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return TaskResponse.model_validate(task)


@router.get("/{task_public_id}", response_model=TaskResponse)
def get_task(
    task_public_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task_or_404(task_public_id, db, current_user)
    return TaskResponse.model_validate(task)


@router.put("/{task_public_id}", response_model=TaskResponse)
def update_task(
    task_public_id: UUID,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task_or_404(task_public_id, db, current_user)
    updates = task_in.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return TaskResponse.model_validate(task)


@router.delete("/{task_public_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_public_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task_or_404(task_public_id, db, current_user)
    task.is_deleted = True
    db.commit()
