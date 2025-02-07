# fastapi-learn
Learning FastAPI and it's capabilities

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

