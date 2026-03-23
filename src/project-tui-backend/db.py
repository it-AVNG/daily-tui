from __future__ import annotations
from sqlmodel import Field, SQLModel, create_engine, Relationship
from datetime import datetime
from enum import Enum


class Status(Enum):
    COMPLETED = 0
    PLANNED = 1
    PROGRRESSING = 2
    LATE = 3


class Warnings(Enum):
    HIGH_RISK = 2
    LOW_RISK = 1
    ON_TIME = 0


class TaskInterlink(SQLModel, table=True):
    root_task_id: int | None = Field(
        default=None, foreign_key="tasks.id", primary_key=True
    )
    follow_task_id: int | None = Field(
        default=None, foreign_key="tasks.id", primary_key=True
    )


class Tasks(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    start_time: datetime
    eta: float
    warning: Warnings
    status: Status

    root_task: list["Tasks"] = Relationship(
        back_populates="follow_by", link_model=TaskInterlink
    )
    follow_by: list["Tasks"] = Relationship(
        back_populates="root_task", link_model=TaskInterlink
    )

    project_id: int | None = Field(default=None, foreign_key="projects.id")


class Projects(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    warning: Warnings
    status: Status


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)
