from dataclasses import dataclass,field
from enum import Enum
from datetime import datetime


class Status(Enum):
    COMPLETED = 0
    PLANNED = 1
    PROGRRESSING = 2
    LATE = 3


class Risk(Enum):
    HIGH_RISK = 2
    LOW_RISK = 1
    ON_TIME = 0

@dataclass
class Task:
    id:int
    name: str
    description: str
    start_time: datetime
    eta: float
    risk: Risk
    status: Status

    parent_tasks: set[int] = field(default_factory=set)
    child_tasks: set[int] = field(default_factory=set)

    def add_dependencies(self, task_id: int):
        if self.id == task_id:
            raise ValueError('The task can not depend on itself')
        self.parent_tasks.add(task_id)

    def remove_dependencies(self, task_id: int):
        if task_id in self.parent_tasks:
            self.parent_tasks.remove(task_id)
        
    def add_child(self, task_id:int):
        if self.id == task_id:
            raise ValueError('The task can not depend on itself')
        self.child_tasks.add(task_id)

    def remove_child(self, task_id: int):
        if task_id in self.child_tasks:
            self.child_tasks.remove(task_id)

    def set_completed(self):
        self.status = Status.COMPLETED
    
    def _set_late(self):
        self.status = Status.LATE
    
    def _set_progress(self):
        self.status = Status.PROGRRESSING

    def increse_Risk(self):
        match self.risk:
            case Risk.ON_TIME:
                self.risk = Risk.LOW_RISK
            case Risk.LOW_RISK:
                self.risk = Risk.HIGH_RISK
            case _:
                pass

    def decrese_Risk(self):
        match self.risk:
            case Risk.HIGH_RISK:
                self.risk = Risk.LOW_RISK
            case Risk.LOW_RISK:
                self.risk = Risk.ON_TIME
            case _:
                pass
    

@dataclass
class Project:
    id: int
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    risk: Risk
    status: Status

    tasks_id: set[int]
