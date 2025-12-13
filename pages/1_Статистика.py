import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Детальная статистика",
    page_icon="📊",
    layout="wide"
)

st.title("Детальная статистика")

# Тестовые данные
def get_test_progress_data(days=30):
    """Генерируем тестовые данные"""
    data = []
    for i in range(days, 0, -1):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        points = 100 + (30 - i) * 5 + (i % 7) * 20
        data.append({"date": date, "points": max(50, points)})
    return data

def get_activity_data():
    return {
        "Бег": 45,
        "Плавание": 30, 
        "Велосипед": 15,
        "Силовая тренировка": 10
    }

def get_weekly_data():
    return [
        {"week": "Неделя 1", "total_points": 500},
        {"week": "Неделя 2", "total_points": 620},
        {"week": "Неделя 3", "total_points": 580},
        {"week": "Неделя 4", "total_points": 720}
    ]

# Основной контент
try:
    from modules.charts import (
        create_progress_chart, 
        create_activity_distribution_chart,
        create_weekly_comparison_chart
    )
    
    # Фильтры
    col1, col2 = st.columns(2)
    with col1:
        period = st.selectbox(
            "Период",
            ["7 дней", "30 дней", "90 дней"],
            index=1
        )
    
    days_map = {"7 дней": 7, "30 дней": 30, "90 дней": 90}
    selected_days = days_map[period]
    
    # Вкладки
    tab1, tab2, tab3 = st.tabs(["Прогресс", "Распределение", "Сравнение"])
    
    with tab1:
        st.header("Прогресс по дням")
        
        # Получаем данные
        progress_data = get_test_progress_data(selected_days)
        
        # Создаем график
        fig = create_progress_chart(
            progress_data, 
            title=f"Прогресс ({period})"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Статистика
        points = [d["points"] for d in progress_data]
        st.subheader("Ключевые метрики")
        cols = st.columns(3)
        with cols[0]:
            st.metric("Среднее", f"{sum(points)//len(points)}")
        with cols[1]:
            st.metric("Максимум", f"{max(points)}")
        with cols[2]:
            st.metric("Всего", f"{sum(points)}")
    
    with tab2:
        st.header("Распределение по активностям")
        
        activity_data = get_activity_data()
        fig = create_activity_distribution_chart(activity_data)
        st.plotly_chart(fig, use_container_width=True)
        
        # Таблица
        st.subheader("Детализация")
        for activity, points in activity_data.items():
            st.write(f"**{activity}:** {points} очков")
    
    with tab3:
        st.header("Сравнение по неделям")
        
        weekly_data = get_weekly_data()
        fig = create_weekly_comparison_chart(weekly_data)
        st.plotly_chart(fig, use_container_width=True)
        
        # Анализ роста
        points = [w["total_points"] for w in weekly_data]
        growth = ((points[-1] - points[0]) / points[0]) * 100
        st.metric(
            "Рост за период", 
            f"{growth:.1f}%", 
            f"{points[-1] - points[0]} очков"
        )
    
    st.success("Статистика загружена успешно!")
    
except ImportError as e:
    st.error(f"Ошибка импорта: {e}. Проверьте файл modules/charts.py")
except Exception as e:
    st.error(f"Ошибка: {e}")

# Футер
st.divider()
st.caption("Данные обновлены: " + datetime.now().strftime("%Y-%m-%d %H:%M"))
