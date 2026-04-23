# flowstate-api

A task manager REST API built with FastAPI and Python. Designed as a test automation target — clean architecture, JWT auth, full CRUD, and auto-generated OpenAPI docs.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | SQLite (via SQLAlchemy ORM) |
| Migrations | Alembic |
| Auth | JWT (python-jose + passlib/bcrypt) |
| Validation | Pydantic v2 |
| Server | Uvicorn |

---

## Project Structure

```
flowstate-api/
├── app/
│   ├── config.py          # Settings loaded from .env
│   ├── database.py        # SQLAlchemy engine, session, Base
│   ├── dependencies.py    # FastAPI DI: get_db(), get_current_user()
│   ├── main.py            # App factory, router registration, /health
│   ├── models/
│   │   ├── user.py        # User ORM model
│   │   └── task.py        # Task ORM model + enums
│   ├── routers/
│   │   ├── auth.py        # POST /auth/register, POST /auth/login
│   │   └── tasks.py       # Full task CRUD
│   └── schemas/
│       ├── auth.py        # Token response schema
│       ├── user.py        # UserCreate, UserResponse
│       └── task.py        # TaskCreate, TaskUpdate, TaskResponse
├── alembic/               # Database migration scripts
├── alembic.ini
├── requirements.txt
├── .env.example
└── FEATURE_BACKLOG.md
```

---

## Local Setup

### 1. Clone and enter the repo

```bash
git clone <repo-url>
cd flowstate-api
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and set a real `SECRET_KEY`:

```bash
openssl rand -hex 32   # paste the output as SECRET_KEY in .env
```

### 5. Create the database

```bash
alembic upgrade head
```

### 6. Run the server

```bash
uvicorn app.main:app --reload
```

The API is now running at `http://localhost:8000`.

---

## Interactive Docs

| URL | Description |
|---|---|
| `http://localhost:8000/docs` | Swagger UI — try every endpoint in the browser |
| `http://localhost:8000/redoc` | ReDoc — clean reference documentation |
| `http://localhost:8000/openapi.json` | Raw OpenAPI spec (used for contract testing) |

---

## API Routes

### Meta

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/health` | No | Returns `{"status": "ok"}` |

### Auth

| Method | Path | Auth | Description |
|---|---|---|---|
| `POST` | `/auth/register` | No | Create a new user account |
| `POST` | `/auth/login` | No | Authenticate and receive a JWT |

> `/auth/login` expects form data (`Content-Type: application/x-www-form-urlencoded`) with fields `username` (email) and `password`.

### Tasks

All task routes require `Authorization: Bearer <token>` header.

| Method | Path | Description |
|---|---|---|
| `GET` | `/tasks` | List all tasks for the current user |
| `POST` | `/tasks` | Create a new task |
| `GET` | `/tasks/{id}` | Get a single task by ID |
| `PUT` | `/tasks/{id}` | Update a task (partial updates supported) |
| `DELETE` | `/tasks/{id}` | Soft-delete a task |

#### Filtering `GET /tasks`

| Query param | Values | Example |
|---|---|---|
| `status` | `todo`, `in_progress`, `done` | `?status=todo` |
| `priority` | `low`, `medium`, `high` | `?priority=high` |

---

## Environment Variables

Defined in `.env` (copy from `.env.example`):

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./flowstate.db` | SQLAlchemy connection string |
| `SECRET_KEY` | *(change this)* | Secret used to sign JWTs — generate with `openssl rand -hex 32` |
| `ALGORITHM` | `HS256` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | How long a token is valid |

---

## Database Migrations

```bash
# Apply all pending migrations (run after clone or model changes)
alembic upgrade head

# Generate a new migration after changing a model
alembic revision --autogenerate -m "describe your change"

# Check current migration state
alembic current
```
