from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from database import get_connection, initialize_database


app = FastAPI()


class Task(BaseModel):
    title: str
    done: bool = False


initialize_database()


@app.get("/tasks")
def get_tasks() -> list[dict]:
    with get_connection() as connection:
        tasks = connection.execute("SELECT * FROM tasks").fetchall()
        return [dict(task) for task in tasks]


@app.get("/tasks/{task_id}")
def get_task(task_id: int) -> dict:
    with get_connection() as connection:
        task = connection.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return dict(task)


@app.post("/tasks", status_code=201)
def create_task(task: Task) -> dict:
    validate_title(task)

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO tasks (title, done)
            VALUES (?, ?)
            """,
            (task.title, task.done),
        )
        created_task = connection.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()

    return dict(created_task)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task) -> dict:
    validate_title(task)

    with get_connection() as connection:
        existing_task = connection.execute(
            "SELECT id FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()
        if existing_task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        connection.execute(
            """
            UPDATE tasks
            SET title = ?, done = ?
            WHERE id = ?
            """,
            (task.title, task.done, task_id),
        )
        updated_task = connection.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()

    return dict(updated_task)


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int) -> None:
    with get_connection() as connection:
        existing_task = connection.execute(
            "SELECT id FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()
        if existing_task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))


def validate_title(task: Task) -> None:
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")
