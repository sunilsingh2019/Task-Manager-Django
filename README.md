# Task-Manager-Django

A robust task management system built with Django, PostgreSQL, and Docker.

## Features

- User Authentication (Login/Register)
- Task Management (Create, Read, Update, Delete)
- Priority and Status tracking
- Task Categories and Tags
- Time Tracking
- File Attachments
- Task Dependencies
- Kanban Board View
- Task Statistics and Reports
- Bootstrap UI with responsive design
- Docker containerization
- PostgreSQL database

## Tech Stack

- Django
- PostgreSQL
- Docker & Docker Compose
- Bootstrap 5
- Font Awesome icons
- Django Summernote (Rich Text Editor)
- Django Filter
- Django Widget Tweaks
- Crispy Forms

## Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose (for Docker installation)
- PostgreSQL (for local installation)
- pip (Python package installer)

## Installation

### Option 1: Docker Installation (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/sunilsingh2019/Task-Manager-Django.git
cd Task-Manager-Django
```

2. Create a `.env` file in the root directory (optional):
```bash
DEBUG=1
SECRET_KEY=your-secret-key-here
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
POSTGRES_DB=task_management
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

3. Build and run with Docker:
```bash
docker-compose up --build
```

4. Create a superuser (in a new terminal):
```bash
docker-compose exec web python manage.py createsuperuser
```

5. Access the application at http://localhost:8000

### Option 2: Local Installation

1. Clone the repository:
```bash
git clone https://github.com/sunilsingh2019/Task-Manager-Django.git
cd Task-Manager-Django
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a PostgreSQL database and update settings:
   - Create a database named 'task_management'
   - Update database settings in core/settings.py if needed

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

8. Access the application at http://localhost:8000

## Environment Variables

The following environment variables can be set in docker-compose.yml or .env file:

- `DEBUG`: Set to 1 for development
- `SECRET_KEY`: Django secret key
- `DJANGO_ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `POSTGRES_DB`: Database name
- `POSTGRES_USER`: Database user
- `POSTGRES_PASSWORD`: Database password

## First Time Setup

1. After installation, log in with your superuser account
2. Create initial categories and tags via the UI
3. Start creating tasks and assigning them to users

## Common Issues and Solutions

### Docker Installation

1. Port conflicts:
   - If port 8000 is already in use, modify the port mapping in docker-compose.yml
   - If PostgreSQL port 5432 is in use, modify the database port mapping

2. Database connection issues:
   - Ensure PostgreSQL container is running: `docker-compose ps`
   - Check logs: `docker-compose logs db`

### Local Installation

1. Database connection issues:
   - Verify PostgreSQL is running
   - Check database credentials in settings.py
   - Ensure database 'task_management' exists

2. Dependencies issues:
   - Upgrade pip: `pip install --upgrade pip`
   - Install system dependencies if needed (e.g., psycopg2 requirements)

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details