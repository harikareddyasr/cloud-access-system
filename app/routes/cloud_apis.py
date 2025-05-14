from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from ..utils.dependencies import get_current_user
from ..database import get_async_session
from ..models import User, Subscription, Plan, UsageLog
import json

router = APIRouter()

def create_cloud_api_route(api_name: str):
    async def api_handler(
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(get_current_user)
    ):
        # Step 1: Get user subscription and pre-load the plan
        result = await db.execute(
            select(Subscription)
            .options(selectinload(Subscription.plan))
            .where(Subscription.user_id == current_user.id)
        )
        subscription = result.scalars().first()
        if not subscription:
            raise HTTPException(status_code=403, detail="No active subscription")

        plan = subscription.plan

        # Step 2: Deserialize API permissions and limits
        api_permissions = plan.api_permissions
        usage_limits = plan.usage_limits

        if isinstance(api_permissions, str):
            api_permissions = json.loads(api_permissions)
        if isinstance(usage_limits, str):
            usage_limits = json.loads(usage_limits)

        # ✅ Step 3: Enforce API access permission
        if api_name not in api_permissions:
            raise HTTPException(status_code=403, detail=f"API '{api_name}' is not allowed in your plan")

        # Step 4: Check current usage
        allowed_limit = usage_limits.get(api_name, 0)
        result = await db.execute(
            select(UsageLog).where(
                UsageLog.user_id == current_user.id,
                UsageLog.api_name == api_name
            )
        )
        usage = result.scalars().first()

        if usage and usage.count >= allowed_limit:
            raise HTTPException(status_code=403, detail=f"API '{api_name}' usage limit exceeded")

        # Step 5: Log usage
        if usage:
            usage.count += 1
        else:
            usage = UsageLog(user_id=current_user.id, api_name=api_name, count=1)
            db.add(usage)

        await db.commit()
        return {"message": f"Welcome to {api_name.upper()}!"}

    return api_handler

# Register 6 fake cloud API routes dynamically
for i in range(1, 7):
    endpoint = f"/cloud/api{i}"
    api_name = f"api{i}"
    router.add_api_route(endpoint, create_cloud_api_route(api_name), methods=["GET"], name=api_name)
