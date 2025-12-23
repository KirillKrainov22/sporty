import httpx
from src.config import API_BASE_URL


class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL.rstrip("/")

    async def _request(self, method: str, path: str, json: dict | None = None):
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.request(method, self.base_url + path, json=json)
            response.raise_for_status()
            return response.json()

    async def create_user(self, telegram_id: int, username: str | None = None):
        return await self._request(
            "POST",
            "/api/users/",
            {"telegram_id": telegram_id, "username": username},
        )

    async def get_user_by_telegram_id(self, telegram_id: int):
        return await self._request("GET", f"/api/users/{telegram_id}")

    async def get_user_stats(self, user_id: int):
        return await self._request("GET", f"/api/users/{user_id}/stats")

    async def get_user_achievements(self, user_id: int):
        return await self._request("GET", f"/api/users/{user_id}/achievements")

    async def create_activity(
        self, user_id: int, type_: str, distance: float | None, duration: int | None
    ):
        return await self._request(
            "POST",
            "/api/activities/",
            {
                "user_id": user_id,
                "type": type_,
                "distance": distance,
                "duration": duration,
            },
        )

    async def add_friend(self, user_id: int, friend_id: int):
        return await self._request(
            "POST", "/api/friends/", {"user_id": user_id, "friend_id": friend_id}
        )

    async def get_user_friends(self, user_id: int):
        return await self._request("GET", f"/api/friends/users/{user_id}")

    async def get_leaderboard(self):
        return await self._request("GET", "/api/leaderboard/")

    async def get_friends_leaderboard(self, user_id: int):
        return await self._request("GET", f"/api/leaderboard/friends/{user_id}")

    async def create_challenge(self, creator_id: int, target_id: int, type_: str):
        return await self._request(
            "POST",
            "/api/challenges/",
            {"creator_id": creator_id, "target_id": target_id, "type": type_},
        )

    async def get_challenge(self, challenge_id: int):
        return await self._request("GET", f"/api/challenges/{challenge_id}")


api_client = APIClient()
