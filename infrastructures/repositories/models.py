from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from enum import Enum
from typing import Optional

class Status(Enum):
    COMPLETED = 0
    PLANNED = 1
    PROGRRESSING = 2
    LATE = 3


class Risks(Enum):
    HIGH_RISK = 2
    LOW_RISK = 1
    ON_TIME = 0


class TaskInterlink(SQLModel, table=True):
    parent_task_id: Optional[int] | None = Field(
        default=None, foreign_key="tasks.id", primary_key=True
    )
    child_task_id: Optional[int] | None = Field(
        default=None, foreign_key="tasks.id", primary_key=True
    )


class Tasks(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    start_time: datetime
    eta: float
    risk: Risks
    status: Status

    # This Task completion is depend on
    parent_tasks: set["Tasks"] = Relationship(
        back_populates="child_tasks", link_model=TaskInterlink, sa_relationship_kwargs={
            # "foreign_keys":"TaskInterlink.parent_task_id"
            "primaryjoin": "Tasks.id==TaskInterlink.child_task_id",
            "secondaryjoin": "Tasks.id==TaskInterlink.parent_task_id",
        }
    )

    # This Task completion is the prerequisite of
    child_tasks: set["Tasks"] = Relationship(
        back_populates="parent_tasks", link_model=TaskInterlink,sa_relationship_kwargs={
            "primaryjoin": "Tasks.id==TaskInterlink.parent_task_id",
            "secondaryjoin": "Tasks.id==TaskInterlink.child_task_id",
        }
    )

    project_id: int | None = Field(default=None, foreign_key="projects.id")


class Projects(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    risk: Risks
    status: Status

