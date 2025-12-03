"""
Модуль для работы с API Person A
ВНИМАНИЕ: Все данные получаем только через API!
"""
import requests
import streamlit as st
from typing import Optional, Dict


class APIClient:
    def __init__(self, base_url: str = "http://api:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def get_user_stats(self, user_id: int) -> Optional[Dict]:
        try:
            response = self.session.get(f"{self.base_url}/api/users/{user_id}/stats")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"API Error: {e}")
            return None

api = APIClient()
