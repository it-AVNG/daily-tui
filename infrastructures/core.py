from sqlmodel import Session, select
from datetime import datetime
from project_tui_backend.models import (
    Projects,
    Tasks,
    Warnings,
    Status,
)
from project_tui_backend.db import create_db_and_table, engine


def create_projects() -> Projects:
    with Session(engine) as session:
        project_starter = Projects(
            name="new_project",
            description="A starter project template",
            start_time=datetime(2026, 12, 12),
            end_time=datetime(2026, 12, 24),
            warning=Warnings.ON_TIME,
            status=Status.PLANNED,
        )
        session.add(project_starter)
        session.commit()
        return project_starter


def create_tasks(parent_project_id: int) -> list[Tasks]:
    target_parent_id = parent_project_id
    with Session(engine) as session:
        parent = session.exec(
            select(Projects).where(Projects.id == target_parent_id)
        ).one()

        task1 = Tasks(
            name="task1",
            description="a 1st stask",
            start_time=datetime(2026, 12, 12),
            eta=9.5,
            warning=Warnings.ON_TIME,
            status=Status.PLANNED,
            project_id=parent.id,
        )
        task2 = Tasks(
            name="task2",
            description="a 2nd stask",
            start_time=datetime(2026, 12, 14),
            eta=2.5,
            warning=Warnings.ON_TIME,
            status=Status.PLANNED,
            project_id=parent.id,
        )
        task3 = Tasks(
            name="task3",
            description="a 3rd stask",
            start_time=datetime(2026, 12, 17),
            eta=5.5,
            warning=Warnings.ON_TIME,
            status=Status.PLANNED,
            project_id=parent.id,
        )
        session.add_all([task1, task2, task3])
        session.commit()

        return [task1, task2, task3]


def create_dependencies(parent_task_id: int, child_task_id: int) -> None:
    with Session(engine) as session:
        parent = session.exec(
            select(Tasks).where(Tasks.id == parent_task_id)
        ).one()
        child = session.exec(
            select(Tasks).where(Tasks.id == child_task_id)
        ).one()
        parent.child_tasks.append(child)
        session.add(parent)
        session.commit()
    return


def main():
    create_db_and_table()
    projects = create_projects()
    print(projects)
    tasks = create_tasks(parent_project_id=1)
    for task in tasks:
        print(task)
    create_dependencies(parent_task_id=1, child_task_id=2)

    with Session(engine) as session:
        task = session.exec(
            select(Tasks).where(Tasks.id == 1)
        ).one()
        print("child task of 1st task:", task.child_tasks)


if __name__ == "__main__":
    main()
