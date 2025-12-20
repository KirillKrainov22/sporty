from fastapi import Header, HTTPException, status

from app.core.config import settings



async def verify_admin_token(x_admin_token: str | None = Header(None)):
    """
    Простая токен-авторизация для админских эндпоинтов.
    Ожидаем заголовок: X-Admin-Token: <token>
    """
    if x_admin_token != settings.ADMIN_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin token",
        )
    return True
#для коммита
