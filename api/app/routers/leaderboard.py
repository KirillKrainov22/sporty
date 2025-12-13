from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, or_
from app.db import get_session
from app.models.user import User
from app.models.friend import Friend
from app.schemas.leaderboard import LeaderboardUser

router = APIRouter(
    prefix="/api/leaderboard",
    tags=["Leaderboard"]
)


# ---------------------------
# 1) ОБЩИЙ ЛИДЕРБОРД
# ---------------------------
@router.get("/", response_model=list[LeaderboardUser])
async def get_global_leaderboard(db: AsyncSession = Depends(get_session)):
    query = (
        select(User.id, User.username, User.points)
        .where(User.is_banned == False)
        .order_by(desc(User.points))
    )
    result = await db.execute(query)
    rows = result.all()

    return [
        LeaderboardUser(
            user_id=row.id,
            username=row.username,
            points=row.points
        )
        for row in rows
    ]


# ---------------------------
# 2) ЛИДЕРБОРД СРЕДИ ДРУЗЕЙ
# ---------------------------
@router.get("/friends/{user_id}", response_model=list[LeaderboardUser])
async def get_friends_leaderboard(user_id: int, db: AsyncSession = Depends(get_session)):

    # Найдём друзей (accepted)
    friends_query = select(Friend).where(
        or_(
            Friend.user_id == user_id,
            Friend.friend_id == user_id
        ),
        Friend.status == "accepted"
    )

    res = await db.execute(friends_query)
    friend_rows = res.scalars().all()

    if not friend_rows:
        return []  # у пользователя пока нет друзей

    # Составим список ID друзей
    friend_ids = []

    for fr in friend_rows:
        if fr.user_id == user_id:
            friend_ids.append(fr.friend_id)
        else:
            friend_ids.append(fr.user_id)

    # запросим пользователей
    users_query = (
        select(User.id, User.username, User.points)
        .where(
            User.id.in_(friend_ids),
            User.is_banned == False
        )
        .order_by(desc(User.points))

    )

    res2 = await db.execute(users_query)
    rows = res2.all()

    return [
        LeaderboardUser(
            user_id=row.id,
            username=row.username,
            points=row.points
        )
        for row in rows
    ]
