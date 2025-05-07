from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

# Database URL
DATABASE_URL = "sqlite+aiosqlite:///./cloudaccess.db"

# Async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Session maker
async_session = async_sessionmaker(engine, expire_on_commit=False)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session

# Optional: used in startup to create tables
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
