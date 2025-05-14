from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils.dependencies import require_admin
from ..schemas.permission import PermissionCreate, PermissionUpdate, PermissionOut
from ..crud.permission import create_permission, update_permission, delete_permission
from ..database import get_async_session

router = APIRouter(prefix="/permissions", tags=["Permissions"])

@router.post("/", response_model=PermissionOut)
async def add_permission(
    permission: PermissionCreate,
    db: AsyncSession = Depends(get_async_session),
    admin_user=Depends(require_admin)
):
    return await create_permission(db, permission)

@router.put("/{permission_id}", response_model=PermissionOut)
async def modify_permission(
    permission_id: int,
    permission: PermissionUpdate,
    db: AsyncSession = Depends(get_async_session),
    admin_user=Depends(require_admin)
):
    return await update_permission(db, permission_id, permission)

@router.delete("/{permission_id}")
async def remove_permission(
    permission_id: int,
    db: AsyncSession = Depends(get_async_session),
    admin_user=Depends(require_admin)
):
    return await delete_permission(db, permission_id)
