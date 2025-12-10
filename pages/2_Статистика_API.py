import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Статистика (реальные данные)",
    page_icon="📊",
    layout="wide"
)

st.title("Статистика с реальными данными")

# Импортируем наш API клиент
try:
    from modules.api_client import APIClient
    from modules.cache import cache_data
    from modules.charts import create_progress_chart
    
    # Инициализируем клиент
    @st.cache_resource
    def get_api_client():
        return APIClient(base_url="http://api:8000")
    
    api = get_api_client()
    
    # ID пользователя
    user_id = st.sidebar.number_input("User ID", min_value=1, value=1, step=1)
    
    # Кнопка обновления
    if st.sidebar.button("Обновить данные"):
        st.cache_data.clear()
        st.rerun()
    
    # Получаем данные с кэшированием
    @st.cache_data(ttl=300)
    def get_user_stats(user_id):
        """Получить статистику пользователя"""
        # TODO: Заменить на реальный вызов API
        # response = api.get_user_stats(user_id)
        
        # Пока используем тестовые данные
        dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30, 0, -1)]
        return [
            {"date": date, "points": 100 + i*5 + (i % 7)*20}
            for i, date in enumerate(dates)
        ]
    
    @st.cache_data(ttl=300)
    def get_activity_distribution(user_id):
        """Распределение активностей"""
        # TODO: Заменить на реальный вызов API
        return {
            "Бег": 45,
            "Плавание": 30,
            "Велосипед": 15,
            "Силовая тренировка": 10
        }
    
    # Основной контент
    tab1, tab2 = st.tabs(["Прогресс", "Распределение"])
    
    with tab1:
        st.header("Прогресс пользователя")
        
        # Получаем данные
        with st.spinner("Загружаем данные..."):
            progress_data = get_user_stats(user_id)
        
        if progress_data:
            # Создаем график
            fig = create_progress_chart(
                progress_data,
                title=f"Прогресс пользователя #{user_id}"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Статистика
            points = [d["points"] for d in progress_data]
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Всего очков", sum(points))
            with col2:
                st.metric("Среднее в день", f"{sum(points)//len(points)}")
            with col3:
                st.metric("Максимум", max(points))
        else:
            st.warning("Данные не найдены. Проверьте ID пользователя.")
    
    with tab2:
        st.header("Распределение активностей")
        
        with st.spinner("Загружаем данные..."):
            activity_data = get_activity_distribution(user_id)
        
        if activity_data:
            from modules.charts import create_activity_distribution_chart
            fig = create_activity_distribution_chart(activity_data)
            st.plotly_chart(fig, use_container_width=True)
            
            # Таблица
            st.subheader("Детализация")
            for activity, points in activity_data.items():
                st.write(f"**{activity}:** {points} очков")
        else:
            st.warning("Данные по активностям не найдены.")
    
    # Информация о подключении
    st.sidebar.divider()
    st.sidebar.caption("API статус: Готов к работе")
    st.sidebar.caption(f"Данные обновлены: {datetime.now().strftime('%H:%M:%S')}")
    
except ImportError as e:
    st.error(f"Ошибка импорта модулей: {e}")
    st.info("Убедитесь что файлы modules/api_client.py и modules/cache.py существуют")
except Exception as e:
    st.error(f"Ошибка: {e}")
    st.info("Проверьте подключение к API")
