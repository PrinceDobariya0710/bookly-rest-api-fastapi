# fastapi-learn
Learning FastAPI and it's capabilities

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

