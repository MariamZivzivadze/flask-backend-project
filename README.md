# Flask Backend Project

A backend API built with Flask, SQLAlchemy, and Bcrypt for password hashing.

## Features
- User signup and login with hashed passwords
- Full CRUD operations (Create, Read, Update, Delete users)
- SQLite database

## Tech Stack
- Python
- Flask
- Flask-SQLAlchemy
- Flask-Bcrypt

## Endpoints
- `POST /api/signup` — create a new user
- `POST /api/login` — authenticate a user
- `GET /api/users` — list all users
- `PUT /api/users/<id>` — update a user
- `DELETE /api/users/<id>` — delete a user
