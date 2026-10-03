# W3 CRUD SQLite

A FastAPI CRUD API backed by SQLite.

## Setup

Create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```powershell
uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive documentation is
available at `http://127.0.0.1:8000/docs`.

On first startup, SQLite creates `tasks.db`, the `tasks` table, and three seed
tasks. Existing rows are preserved on subsequent restarts.

## Endpoints

- `GET /tasks`
- `GET /tasks/{task_id}`
- `POST /tasks` with `{"title": "Task title", "done": false}`
- `PUT /tasks/{task_id}` with `{"title": "Updated title", "done": true}`
- `DELETE /tasks/{task_id}`
