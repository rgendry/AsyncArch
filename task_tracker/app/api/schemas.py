from pydantic import BaseModel
from app.models import Status
from typing import Optional, List


class TaskSchema(BaseModel):
    description: str
    status: Status = Status.ASSIGNED
    assignee: str

    class Config:
        orm_mode = True


class TaskListSchema(BaseModel):
    tasks: Optional[List[TaskSchema]]

    class Config:
        orm_mode = True
