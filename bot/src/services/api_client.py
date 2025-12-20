import httpx
from src.config import API_BASE_URL


class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL

    async def get(self, path: str, params: dict | None = None):
        async with httpx.AsyncClient() as client:
            r = await client.get(self.base_url + path, params=params)
            r.raise_for_status()
            return r.json()

    async def post(self, path: str, json: dict):
        async with httpx.AsyncClient() as client:
            r = await client.post(self.base_url + path, json=json)
            r.raise_for_status()
            return r.json()


api_client = APIClient()
