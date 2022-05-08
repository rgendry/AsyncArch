from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import TaskSchema, TaskListSchema
from app.models import Task, Status
from app.db import get_db


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskSchema)
async def create_task(data: TaskSchema, db: AsyncSession = Depends(get_db),) -> TaskSchema:
    instance = Task(**data.dict())
    await instance.save(db)
    response = TaskSchema.from_orm(instance)
    return response


@router.get("/my/", status_code=status.HTTP_200_OK, response_model=TaskSchema)
async def get_task_list(db: AsyncSession = Depends(get_db),) -> TaskListSchema:
    tasks = await Task.all(db)
    response = TaskListSchema.parse_obj({"tasks": tasks})
    return response


@router.post("{task_id}/complete/", status_code=status.HTTP_200_OK, response_model=TaskSchema)
async def complete_task(task_id: int, db: AsyncSession = Depends(get_db),) -> TaskSchema:
    task = await Task.get_by_id(db, task_id)
    await task.update(db, status=Status.COMPLETED)
    response = TaskSchema.from_orm(task)
    return response
