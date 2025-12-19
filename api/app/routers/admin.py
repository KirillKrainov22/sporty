from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.core.admin_auth import verify_admin_token
from app.schemas.admin import (
    AdminUserBanRequest,
    AdminPointsRequest,
    AdminUserItem,
    AdminSystemStatistics,
)
from app.services import admin as admin_service


router = APIRouter(
    prefix="/api/admin",
    tags=["Admin"],
    dependencies=[Depends(verify_admin_token)],
)


@router.get("/users", response_model=list[AdminUserItem])
async def list_users(db: AsyncSession = Depends(get_session)):

    #Список всех пользователей для админки.
    users = await admin_service.get_all_users(db)
    return users


@router.post("/users/{user_id}/ban", response_model=AdminUserItem)
async def ban_or_unban_user(
    user_id: int,
    payload: AdminUserBanRequest,
    db: AsyncSession = Depends(get_session),
):

    # Бан / разбан пользователя.
    # is_banned = true  -> бан
    # is_banned = false -> разбан

    user = await admin_service.set_ban_status(db, user_id, payload.is_banned)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/points", response_model=AdminUserItem)
async def add_points(
    payload: AdminPointsRequest,
    db: AsyncSession = Depends(get_session),
):

    # Ручное начисление / списание очков.
    # amount может быть отрицательным.

    user = await admin_service.add_points(db, payload.user_id, payload.amount)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.get("/statistics", response_model=AdminSystemStatistics)
async def get_statistics(db: AsyncSession = Depends(get_session)):

    #Общая статистика системы.

    stats = await admin_service.get_system_statistics(db)
    return stats
#для коммита
