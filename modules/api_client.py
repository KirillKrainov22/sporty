import requests
from typing import Optional, Dict, Any
import streamlit as st

class APIClient:
    def __init__(self, base_url: str = "http://api:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.timeout = 10
        
    def _handle_response(self, response):
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {e}")
            return None
    
    def get_user_stats(self, user_id: int) -> Optional[Dict]:
        """Получить статистику пользователя"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/users/{user_id}/stats",
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            st.error(f"Не удалось получить статистику: {e}")
            return None
    
    def get_friends(self, user_id: int) -> Optional[Dict]:
        """Получить список друзей"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/users/{user_id}/friends",
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            st.error(f"Не удалось получить список друзей: {e}")
            return None
    
