from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..utils.dependencies import get_current_user
from ..database import get_async_session
from ..models import User, Subscription, Plan, UsageLog
from sqlalchemy.orm import selectinload

router = APIRouter()

def create_cloud_api_route(api_name: str):
    async def api_handler(
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(get_current_user)
    ):
        # Step 1: Get user subscription
        result = await db.execute(
    select(Subscription)
    .options(selectinload(Subscription.plan))
    .where(Subscription.user_id == current_user.id)
)
        subscription = result.scalars().first()
        if not subscription:
            raise HTTPException(status_code=403, detail="No active subscription")

        # Step 2: Get plan details
        plan = subscription.plan
        allowed_limit = plan.usage_limits.get(api_name, 0)

        # Step 3: Check current usage
        result = await db.execute(
            select(UsageLog).where(
                UsageLog.user_id == current_user.id,
                UsageLog.api_name == api_name
            )
        )
        usage = result.scalars().first()

        if usage and usage.count >= allowed_limit:
            raise HTTPException(status_code=403, detail=f"API '{api_name}' usage limit exceeded")

        # Step 4: Log usage
        if usage:
            usage.count += 1
        else:
            usage = UsageLog(user_id=current_user.id, api_name=api_name, count=1)
            db.add(usage)

        await db.commit()
        return {"message": f"Welcome to {api_name.upper()}!"}

    return api_handler

# Dynamically register routes for 6 APIs
for i in range(1, 7):
    endpoint = f"/cloud/api{i}"
    api_name = f"api{i}"
    router.add_api_route(endpoint, create_cloud_api_route(api_name), methods=["GET"], name=api_name)