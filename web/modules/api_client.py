"""
API Client - All data through API Person A
"""
import os
import requests
import streamlit as st


class APIClient:
    def __init__(self):
        # Different URLs for different environments
        self.base_url = os.getenv(
            "API_URL", 
            "http://localhost:8000"  # Local development
        )
        # In Docker compose: "http://api:8000"
        self.session = requests.Session()
    
    def _request(self, endpoint):
        try:
            response = self.session.get(
                f"{self.base_url}{endpoint}", 
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to API.")
            return None
        except Exception as e:
            st.error(f"⚠️ API Error")
            return None
    
    # User methods
    def get_user_stats(self, user_id):
        return self._request(f"/api/users/{user_id}/stats")
    
    def get_user_friends(self, user_id):
        return self._request(f"/api/users/{user_id}/friends")
    
    def get_user_achievements(self, user_id):
        return self._request(f"/api/users/{user_id}/achievements")
    
    # Admin methods
    def get_system_stats(self):
        return self._request("/api/admin/stats")
    
    def search_users(self, query):
        return self._request(f"/api/admin/users/search?q={query}")
    
    def update_user_points(self, user_id, points, reason):
        data = {"points": points, "reason": reason}
        try:
            response = self.session.post(
                f"{self.base_url}/api/admin/users/{user_id}/points",
                json=data,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except:
            return None

api = APIClient()
