# Task-Manager-Django

A robust task management system built with Django, PostgreSQL, and Docker.

## Features

- User Authentication (Login/Register)
- Task Management (Create, Read, Update, Delete)
- Priority and Status tracking
- Bootstrap UI with responsive design
- Docker containerization
- PostgreSQL database

## Tech Stack

- Django
- PostgreSQL
- Docker & Docker Compose
- Bootstrap 5
- Font Awesome icons

## Setup

1. Clone the repository:
```bash
git clone https://github.com/sunilsingh2019/Task-Manager-Django.git
```

2. Run with Docker:
```bash
docker-compose up --build
```

3. Access the application at http://localhost:8000

## Environment Variables

The following environment variables can be set in docker-compose.yml:

- `DEBUG`: Set to 1 for development
- `SECRET_KEY`: Django secret key
- `DJANGO_ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `POSTGRES_DB`: Database name
- `POSTGRES_USER`: Database user
- `POSTGRES_PASSWORD`: Database password