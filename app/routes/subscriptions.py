from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_async_session
from ..crud.subscription import create_subscription, get_all_subscriptions
from ..schemas.subscription import SubscriptionCreate, SubscriptionRead

router = APIRouter()

@router.post("/subscriptions/", response_model=SubscriptionRead)
async def create(subscription: SubscriptionCreate, db: AsyncSession = Depends(get_async_session)):
    return await create_subscription(db, subscription)

@router.get("/subscriptions/", response_model=list[SubscriptionRead])
async def read_all(db: AsyncSession = Depends(get_async_session)):
    return await get_all_subscriptions(db)


