

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .. import models
from app.schemas.subscription import SubscriptionCreate


async def create_subscription(db: AsyncSession, subscription: SubscriptionCreate):
    db_subscription = models.Subscription(**subscription.dict())
    db.add(db_subscription)
    await db.commit()
    await db.refresh(db_subscription)
    return db_subscription

async def get_all_subscriptions(db: AsyncSession):
    result = await db.execute(select(models.Subscription))
    return result.scalars().all()


