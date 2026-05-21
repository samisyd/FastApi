# FastAPI Blog with Database

A minimal FastAPI blog example using SQLAlchemy and SQLite, with both HTML page views and JSON API endpoints.

## Features

- SQLite database backend via SQLAlchemy
- User and post models with one-to-many relationship
- HTML templates for home page, post detail, and user posts
- REST API for users and posts
- Error handling for API and HTML requests
- Static files support for CSS, JS, and media uploads

## Requirements

- Python 3.12+
- `fastapi[standard]`
- `sqlalchemy`

## Install

```powershell
python -m pip install -r requirements.txt
```

If you use the `pyproject.toml` dependencies instead:

```powershell
python -m pip install fastapi[standard] sqlalchemy
```

## Run the app

```powershell
uvicorn main:app --reload
```

Then open:

- `http://127.0.0.1:8000/` for the home page
- `http://127.0.0.1:8000/docs` for the interactive OpenAPI docs

## Database

The SQLite database file is created automatically as `blog.db` in the project root.

## App structure

- `main.py` - FastAPI application, HTML routes, and API routes
- `database.py` - SQLAlchemy engine, session, and base model setup
- `models.py` - SQLAlchemy ORM models for `User` and `Post`
- `schemas.py` - Pydantic request and response schemas
- `templates/` - Jinja2 HTML templates
- `static/` - CSS, JavaScript, and manifest assets
- `media/` - Profile picture uploads and media files

## API endpoints

### Users

- `POST /api/users` - create a user
- `GET /api/users/{user_id}` - fetch a user
- `PATCH /api/users/{user_id}` - update a user
- `DELETE /api/users/{user_id}` - delete a user
- `GET /api/users/{user_id}/posts` - fetch posts for a user

### Posts

- `GET /api/posts` - fetch all posts
- `POST /api/posts` - create a post
- `GET /api/posts/{post_id}` - fetch a single post
- `PUT /api/posts/{post_id}` - replace a post
- `PATCH /api/posts/{post_id}` - partially update a post
- `DELETE /api/posts/{post_id}` - delete a post

## Example request bodies

### Create user

```json
{
  "username": "alice",
  "email": "alice@example.com"
}
```

### Create post

```json
{
  "title": "My first post",
  "content": "Hello world!",
  "user_id": 1
}
```

## Notes

- The `User` model supports an optional `image_file` field and provides an `image_path` property for profile pictures.
- Deleting a user removes their posts via cascade delete.
- Custom exception handlers return JSON errors for `/api` routes and HTML error pages for browser requests.
