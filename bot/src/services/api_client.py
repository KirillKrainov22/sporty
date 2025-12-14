import requests
from src.config import API_BASE_URL

DEFAULT_TIMEOUT = 5


class ApiError(Exception):
    def __init__(self, status_code: int, message: str = ""):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API error {status_code}: {message}")


def _handle(resp: requests.Response):
    # если API вернул ошибку — бросаем ApiError, чтобы хендлер решил, что писать юзеру
    if 200 <= resp.status_code < 300:
        return resp.json() if resp.content else None
    try:
        detail = resp.json()
    except Exception:
        detail = resp.text
    raise ApiError(resp.status_code, str(detail))


def create_user(telegram_id: int, username: str | None):
    """
    POST /api/users/
    Если юзер уже есть — API вернёт 400 (по доке Кирилла).
    """
    url = f"{API_BASE_URL}/api/users/"
    payload = {"telegram_id": telegram_id, "username": username}
    resp = requests.post(url, json=payload, timeout=DEFAULT_TIMEOUT)
    return _handle(resp)


def get_user_by_telegram_id(telegram_id: int):
    """
    GET /api/users/{telegram_id}
    """
    url = f"{API_BASE_URL}/api/users/{telegram_id}"
    resp = requests.get(url, timeout=DEFAULT_TIMEOUT)
    return _handle(resp)


def ensure_user(telegram_id: int, username: str | None):
    """
    Гарантирует, что user существует и возвращает объект пользователя.
    Логика:
    - пытаемся создать
    - если "уже существует" -> получаем по telegram_id
    """
    try:
        return create_user(telegram_id, username)
    except ApiError as e:
        if e.status_code == 400:
            return get_user_by_telegram_id(telegram_id)
        raise


def create_activity(user_id: int, activity_type: str, distance: float, duration_seconds: int):
    """
    POST /api/activities/
    """
    url = f"{API_BASE_URL}/api/activities/"
    payload = {
        "user_id": user_id,
        "type": activity_type,
        "distance": distance,
        "duration": duration_seconds
    }
    resp = requests.post(url, json=payload, timeout=DEFAULT_TIMEOUT)
    return _handle(resp)


def get_user_stats(user_id: int):
    """
    GET /api/users/{user_id}/stats
    """
    url = f"{API_BASE_URL}/api/users/{user_id}/stats"
    resp = requests.get(url, timeout=DEFAULT_TIMEOUT)
    return _handle(resp)


def get_leaderboard():
    """
    GET /api/leaderboard/
    """
    url = f"{API_BASE_URL}/api/leaderboard/"
    resp = requests.get(url, timeout=DEFAULT_TIMEOUT)
    return _handle(resp)


def get_friends(user_id: int):
    """
    GET /api/friends/users/{user_id}
    """
    url = f"{API_BASE_URL}/api/friends/users/{user_id}"
    resp = requests.get(url, timeout=DEFAULT_TIMEOUT)
    return _handle(resp)


def add_friend(user_id: int, friend_id: int):
    """
    POST /api/friends/
    """
    url = f"{API_BASE_URL}/api/friends/"
    payload = {"user_id": user_id, "friend_id": friend_id}
    resp = requests.post(url, json=payload, timeout=DEFAULT_TIMEOUT)
    return _handle(resp)
