from sqlalchemy import text

async def get_achievement_id_by_code(session, code: str) -> int | None:
    res = await session.execute(
        text("SELECT id FROM achievements WHERE code = :code AND is_active = true"),
        {"code": code},
    )
    row = res.first()
    return row[0] if row else None


async def user_has_achievement(session, user_id: int, achievement_id: int) -> bool:
    res = await session.execute(
        text("""
            SELECT 1
            FROM user_achievements
            WHERE user_id = :uid AND achievement_id = :aid
        """),
        {"uid": user_id, "aid": achievement_id},
    )
    return res.first() is not None


async def grant_achievement(session, user_id: int, achievement_id: int) -> bool:
    """
    Возвращает True если реально выдали (вставили),
    False если уже было (или конфликт).
    """
    res = await session.execute(
        text("""
            INSERT INTO user_achievements(user_id, achievement_id)
            VALUES (:uid, :aid)
            ON CONFLICT DO NOTHING
            RETURNING id
        """),
        {"uid": user_id, "aid": achievement_id},
    )
    return res.first() is not None