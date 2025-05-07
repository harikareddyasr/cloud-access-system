from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.user import UserCreate, UserRead
from ..crud.user import create_user, get_all_users
from ..database import async_session

router = APIRouter(prefix="/users", tags=["Users"])

# Dependency to get DB session
async def get_db():
    async with async_session() as session:
        yield session

@router.post("/", response_model=UserRead)
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(user, db)

@router.get("/", response_model=list[UserRead])
async def list_all_users(db: AsyncSession = Depends(get_db)):
    return await get_all_users(db)
