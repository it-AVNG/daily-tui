from sqlmodel import Session
from datetime import datetime
from project_tui_backend.models import (
    Projects,
    TaskInterlink,
    Tasks,
    Warnings,
    Status,
)
from project_tui_backend.db import create_db_and_table, engine


def create_projects():
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


def create_tasks():
    pass


def create_dependencies():
    pass


def main():
    create_db_and_table()
    projects = create_projects()
    print(projects)
    create_tasks()
    create_dependencies()


if __name__ == "__main__":
    main()
