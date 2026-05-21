# FastAPI Authentication Example

A minimal FastAPI authentication project using JWTs, password hashing, and SQLAlchemy.

## Features

- User registration endpoint
- Login endpoint returning JWT access tokens
- Protected endpoint requiring Bearer auth
- SQLite database via SQLAlchemy
- Password hashing using `pwdlib`
- Environment-based JWT settings

## Requirements

- Python 3.13+
- Dependencies defined in `pyproject.toml`

## Installation

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate it:

Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install -U pip
pip install -e .
```

## Configuration

Create a `.env` file in the project root with these values:

```env
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Optionally change `DATABASE_URL` in `database.py` if you want a different database.

## Running the app

Start the FastAPI app with:

```bash
uvicorn main:app --reload
```

The API docs are available at:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## API Endpoints

### Register a new user

`POST /auth/register`

Request body:

```json
{
  "username": "exampleuser",
  "email": "user@example.com",
  "password": "strongpassword"
}
```

Response:

```json
{
  "message": "User created successfully"
}
```

### Login and receive a JWT

`POST /auth/token`

Form data:

- `username`
- `password`

Response:

```json
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
```

### Protected root endpoint

`GET /`

Requires `Authorization: Bearer <access_token>` header.

Response example:

```json
{
  "User": {
    "id": 1,
    "username": "exampleuser",
    "email": "user@example.com",
    "hashed_password": "..."
  }
}
```

## Project structure

- `main.py` - app entry point and protected root route
- `auth.py` - registration, login, JWT creation, and current user dependency
- `models.py` - SQLAlchemy `User` model
- `database.py` - database engine, session, and dependency helper
- `pyproject.toml` - project metadata and dependencies

## Notes

- The project currently uses SQLite by default (`todosapp.db`).
- Keep `SECRET_KEY` secure and do not commit it to source control.
- For production, use a stronger database configuration and HTTPS.
