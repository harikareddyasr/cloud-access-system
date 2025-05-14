from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List

from app.database import get_async_session
from app.utils.dependencies import get_current_user
from app.models import User, Plan, Subscription, UsageLog

router = APIRouter(prefix="/cloud", tags=["Cloud Services"])


# ✅ Helper function to check API access and usage limits
def check_permission_and_usage(plan: Plan, api: str, usage_logs: List[UsageLog]):
    if api not in plan.api_permissions:
        raise HTTPException(status_code=403, detail=f"Access denied to {api}")

    used_count = sum(log.count for log in usage_logs if log.api_name == api)
    allowed = plan.usage_limits.get(api, 0)

    if used_count >= allowed:
        raise HTTPException(status_code=403, detail=f"Usage limit exceeded for {api}")

    return used_count, allowed


# ✅ Shared logic to handle cloud API access
async def access_cloud_api(user_id: int, api: str, db: AsyncSession):
    result = await db.execute(
        select(Subscription)
        .options(selectinload(Subscription.plan))
        .where(Subscription.user_id == user_id)
    )
    subscription = result.scalars().first()
    if not subscription or not subscription.plan:
        raise HTTPException(status_code=404, detail="Subscription or plan not found")

    plan = subscription.plan

    usage_result = await db.execute(
        select(UsageLog).where(
            UsageLog.user_id == user_id,
            UsageLog.api_name == api
        )
    )
    logs = usage_result.scalars().all()

    used_count, allowed = check_permission_and_usage(plan, api, logs)

    # Record new usage
    usage_log = UsageLog(user_id=user_id, api_name=api, count=1)
    db.add(usage_log)
    await db.commit()

    return {
        "message": f"{api} accessed successfully",
        "used": used_count + 1,
        "allowed": allowed
    }


# ✅ Dynamic route creation for 6 APIs
def create_cloud_api_route(api_name: str):
    async def handler(
        user_id: int,
        db: AsyncSession = Depends(get_async_session),
        _: User = Depends(get_current_user),
    ):
        return await access_cloud_api(user_id, api_name, db)

    path = f"/{api_name}/{{user_id}}"
    router.add_api_route(path, handler, methods=["GET"], summary=f"Access {api_name.upper()}")


# ✅ Register all 6 APIs
for i in range(1, 7):
    create_cloud_api_route(f"api{i}")
