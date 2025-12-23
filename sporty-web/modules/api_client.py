import os
import requests
import streamlit as st
from modules.config import ADMIN_TOKEN


class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def create_user(self, telegram_id: int, username: str | None = None):
        return self._post(
            "/api/users/",
            {
                "telegram_id": telegram_id,
                "username": username,
            },
        )

    def get_user_by_telegram_id(self, telegram_id: int):
        return self._get(f"/api/users/{telegram_id}")

    def get_user_stats(self, user_id: int):
        return self._get(f"/api/users/{user_id}/stats")

    def get_user_achievements(self, user_id: int):
        return self._get(f"/api/users/{user_id}/achievements")

    def create_activity(
        self, user_id: int, type_: str, distance: float | None, duration: int | None
    ):
        return self._post(
            "/api/activities/",
            {
                "user_id": user_id,
                "type": type_,
                "distance": distance,
                "duration": duration,
            },
        )

    def add_friend(self, user_id: int, friend_id: int):
        return self._post(
            "/api/friends/",
            {
                "user_id": user_id,
                "friend_id": friend_id,
            },
        )

    def get_user_friends(self, user_id: int):
        return self._get(f"/api/friends/users/{user_id}")

    def create_challenge(self, creator_id: int, target_id: int, type_: str):
        return self._post(
            "/api/challenges/",
            {
                "creator_id": creator_id,
                "target_id": target_id,
                "type": type_,
            },
        )

    def get_challenge(self, challenge_id: int):
        return self._get(f"/api/challenges/{challenge_id}")

    def get_global_leaderboard(self):
        return self._get("/api/leaderboard/")

    def get_friends_leaderboard(self, user_id: int):
        return self._get(f"/api/leaderboard/friends/{user_id}")

    def get_admin_users(self, admin_token: str):
        return self._get("/api/admin/users", admin_token=admin_token)

    def ban_user(self, user_id: int, is_banned: bool, admin_token: str):
        return self._post(
            f"/api/admin/users/{user_id}/ban",
            {"is_banned": is_banned},
            admin_token=admin_token,
        )

    def update_user_points(self, user_id: int, amount: int, admin_token: str):
        return self._post(
            "/api/admin/points",
            {
                "user_id": user_id,
                "amount": amount,
            },
            admin_token=admin_token,
        )

    def get_admin_statistics(self, admin_token: str):
        return self._get("/api/admin/statistics", admin_token=admin_token)

    def _get(self, path: str, admin_token: str | None = None):
        headers = self._build_headers(admin_token)
        try:
            r = requests.get(f"{self.base_url}{path}", timeout=10, headers=headers)
            if r.status_code == 200:
                return r.json()
            st.warning(f"API GET {path} -> {r.status_code}")
            return None
        except Exception as e:
            st.error(f"API GET error: {e}")
            return None

    def _post(self, path: str, data: dict, admin_token: str | None = None):
        headers = self._build_headers(admin_token)
        try:
            r = requests.post(
                f"{self.base_url}{path}", json=data, timeout=10, headers=headers
            )
            if r.status_code == 200:
                return r.json()
            st.warning(f"API POST {path} -> {r.status_code}: {r.text}")
            return None
        except Exception as e:
            st.error(f"API POST error: {e}")
            return None

    def _build_headers(self, admin_token: str | None):
        headers = {}
        token = admin_token or ADMIN_TOKEN
        if token:
            headers["X-Admin-Token"] = token
        return headers


BASE_URL = os.environ.get("API_BASE_URL", "http://api:8000")
api = APIClient(base_url=BASE_URL)
