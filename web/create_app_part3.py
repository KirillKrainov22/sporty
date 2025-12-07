with open('app.py', 'a', encoding='utf-8') as f:
    f.write("""

# Main content - Data loading
st.markdown("## Загрузка данных")

try:
    # Try to get real data (cached)
    user_stats = api.get_user_stats(user_id)
    
    # Fallback to mock data if API unavailable
    if user_stats is None:
        st.info("Используем тестовые данные (API временно недоступно)")
        user_stats = MOCK_DATA["user_stats"](user_id)
    
    # Calculate metrics
    metrics = calculate_metrics(user_stats)
    
except Exception as e:
    st.error(f"Ошибка загрузки данных: {e}")
    # Fallback to mock data
    user_stats = MOCK_DATA["user_stats"](user_id)
    metrics = calculate_metrics(user_stats)""")
