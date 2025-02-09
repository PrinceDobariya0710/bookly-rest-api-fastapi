# fastapi-learn
Learning FastAPI and it's capabilities

# Main Libraries and frameworks used for this project
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLModel](https://img.shields.io/badge/SQLModel-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)
![Celery Flower](https://img.shields.io/badge/Celery_Flower-FFDD57?style=for-the-badge&logo=flower&logoColor=black)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NeonDB](https://img.shields.io/badge/NeonDB-000000?style=for-the-badge&logo=neondatabase&logoColor=white)

# Create virtual environment
```bash
python3 -m venv venv
```

# Activate virtual environment for Windows
```bash
venv\Scripts\activate
```

# Run fastapi in development mode
```bash
fastapi dev src
```

# Install dependencies
```bash
pip install -r requirements.txt
```

# Start alembic environment
```bash
pip install alembic
```
## setup migrations
```bash
alembic init -t async migrations
```
## setup env , alembic.ini and mako file
## create revision
```bash
alembic revision --autogenerate -m "init"
```
It will create migration file migrations folder

## apply migrations
```bash
alembic upgrade head
```

# Run celery
```
celery -A src.celery_tasks.c_app worker -l info --pool=solo
```
# Run celery flower
```
celery -A src.celery_tasks.c_app flower
```

# Run Pytest
```
pytest
```

# Run Schemathesis It will generate automatic test cases
## https://schemathesis.readthedocs.io/en/stable/
```
st run http://localhost:8000/api/v1/openapi.json --experimental=openapi-3.1
```

# Use Render to host for free
You can host fastapi, redis and postgresql server for free with limited resources.

# To run fastapi in production environment
```bash
fastapi run src
```

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

```bash
DATABASE_URL = "postgresql+asyncpg://<username>:<password>@<hostname>:5432/bookly_db"
JWT_SECRET_KEY = "testkey"
JWT_ALGORITHM= "HS256"
REDIS_URL=redis://localhost:6379
MAIL_USERNAME="test@gmail.com"
MAIL_PASSWORD="test"
MAIL_FROM="test@gmail.com"
MAIL_PORT=587
MAIL_SERVER="smtp.gmail.com"
MAIL_FROM_NAME="Bookly"
DOMAIN="localhost:8000"
```

# Helpful command to get all installed library versions on your local
```bash
pip freeze > build_requirements.txt
```

# OpenAPI documentation screenshot
![Project Screenshot](https://raw.githubusercontent.com/PrinceDobariya0710/bookly-rest-api-fastapi/refs/heads/main/screencapture-localhost-8000-api-v1-docs-2025-02-09-17_26_29.png)

