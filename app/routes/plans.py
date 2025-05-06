from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.plan import PlanCreate, PlanRead
from ..crud.plan import create_plan, get_all_plans
from ..database import async_session

router = APIRouter(prefix="/plans", tags=["Plans"])

# Dependency to get DB session
async def get_db():
    async with async_session() as session:
        yield session

@router.post("/", response_model=PlanRead)
async def create_new_plan(plan: PlanCreate, db: AsyncSession = Depends(get_db)):
    return await create_plan(plan, db)

@router.get("/", response_model=list[PlanRead])
async def list_all_plans(db: AsyncSession = Depends(get_db)):
    return await get_all_plans(db)
