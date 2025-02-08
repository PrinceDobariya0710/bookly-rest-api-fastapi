from sqlmodel import create_engine,text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.db.models import Book #this import is important 
from src.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

async_engine = AsyncEngine(
    create_engine(
    url=Config.DATABASE_URL,
    echo=True
))

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    """Dependency to provide the session object"""
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session