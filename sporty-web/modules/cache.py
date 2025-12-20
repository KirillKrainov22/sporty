from datetime import datetime, timedelta
import streamlit as st
import hashlib

def cache_data(ttl: int = 300):
    """Декоратор для кэширования данных API"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Создаем ключ кэша
            cache_key = f"{func.__name__}_{hashlib.md5(str(args + tuple(kwargs.items())).encode()).hexdigest()}"
            
            # Проверяем кэш
            if cache_key in st.session_state:
                cached_data, timestamp = st.session_state[cache_key]
                if datetime.now() - timestamp < timedelta(seconds=ttl):
                    return cached_data
            
            # Если нет в кэше или устарел - вызываем функцию
            result = func(*args, **kwargs)
            
            # Сохраняем в кэш
            if result is not None:
                st.session_state[cache_key] = (result, datetime.now())
            
            return result
        return wrapper
    return decorator
