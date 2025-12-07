"""
Caching module for API responses
Uses Streamlit session_state for in-memory cache
"""
from datetime import datetime, timedelta
from typing import Any, Optional, Callable
import streamlit as st
import hashlib
import json


class Cache:
    """Simple TTL cache using Streamlit session state"""
    
    def __init__(self, ttl_seconds: int = 300):
        self.ttl = ttl_seconds
    
    def _get_cache_key(self, func_name: str, *args, **kwargs) -> str:
        """Generate unique cache key from function and arguments"""
        key_data = f"{func_name}_{str(args)}_{str(kwargs)}"
        return f"cache_{hashlib.md5(key_data.encode()).hexdigest()}"
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value if not expired"""
        if key not in st.session_state:
            return None
        
        cached_data = st.session_state[key]
        if not isinstance(cached_data, tuple) or len(cached_data) != 2:
            return None
        
        value, timestamp = cached_data
        if datetime.now() - timestamp > timedelta(seconds=self.ttl):
            del st.session_state[key]  # Remove expired cache
            return None
        
        return value
    
    def set(self, key: str, value: Any):
        """Cache value with timestamp"""
        st.session_state[key] = (value, datetime.now())
    
    def clear(self, pattern: str = "cache_"):
        """Clear all cache or specific pattern"""
        keys_to_delete = [k for k in st.session_state.keys() if k.startswith(pattern)]
        for key in keys_to_delete:
            del st.session_state[key]

# Global cache instance (5 minutes TTL)
cache = Cache(ttl_seconds=300)

def cached(ttl: int = 300):
    """
    Decorator for caching function results
    
    Usage:
    @cached(ttl=300)
    def get_user_stats(user_id):
        # API call here
    """
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            cache_key = f"cache_{func.__name__}_{hashlib.md5(str(args + tuple(kwargs.items())).encode()).hexdigest()}"
            
            # Try cache first
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Call function if not in cache
            result = func(*args, **kwargs)
            
            # Cache result if not None
            if result is not None:
                cache.set(cache_key, result)
            
            return result
        return wrapper
    return decorator
