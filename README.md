# Flask Backend Project

A backend API built with Flask, Flask-SQLAlchemy, and Flask-Bcrypt, featuring authentication, custom exception handling, rate limiting, automated tests, and a CI/CD pipeline — containerized with Docker and deployed live.

## Live Demo

🔗 https://flask-backend-project-8gwj.onrender.com

(Hosted on Render's free tier — the first request after a period of inactivity may take up to 50 seconds to respond while the instance spins back up.)

## Features

- User signup and login with Bcrypt password hashing
- Custom exception handling with correct HTTP status codes (401 Unauthorized, 409 Conflict, 201 Created)
- Rate limiting on login (5 requests/minute) to mitigate brute-force attacks
- Input validation — malformed or missing request data returns a clean 400 response instead of crashing
- SQLite database via the Flask-SQLAlchemy ORM
- Automated test suite (pytest) covering signup, login, and edge cases
- CI pipeline (GitHub Actions) running Pylint on every push
- Containerized with Docker; deployed on Render

## Tech Stack

- Python
- Flask (Blueprints)
- Flask-SQLAlchemy
- Flask-Bcrypt
- Flask-Limiter
- pytest
- Docker
- GitHub Actions (CI)

## Endpoints

- `POST /api/signup` — create a new user
- `POST /api/login` — authenticate a user (rate-limited)
- `GET /api/users` — list all users

## Running Locally

\`\`\`bash
git clone https://github.com/MariamZivzivadze/flask-backend-project.git
cd flask-backend-project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# create a .env file with SECRET_KEY and DATABASE_URL
python3 app.py
\`\`\`

## Running with Docker

\`\`\`bash
docker build -t flask-backend-project .
docker run --env-file .env -p 5000:5000 flask-backend-project
\`\`\`

## Running Tests

\`\`\`bash
pytest
\`\`\`
