import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Our modules
from modules.api_client import api
from modules.cache import cache
from modules.mock_data import MOCK_DATA
from modules.data_utils import prepare_chart_data, calculate_metrics, format_activity_data

# Page config
st.set_page_config(
    page_title="Sporty Dashboard",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Sporty Dashboard")
st.markdown("### Статистика активности")

# Sidebar
with st.sidebar:
    st.markdown("### Настройки")
    
    user_id = st.number_input("ID пользователя", min_value=1, value=1)
    
    st.markdown("---")
    st.markdown("### Управление кэшем")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Обновить данные", type="primary"):
            cache.clear()
            st.rerun()
    
    with col2:
        if st.button("Очистить кэш API"):
            api.clear_cache()
            st.rerun()

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
    metrics = calculate_metrics(user_stats)

# Metrics cards
st.markdown("## Основные показатели")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Всего очков",
        value=f"{metrics.get('total_points', 0):,}",
        delta=f"+{metrics.get('daily_average', 0):.0f} в день"
    )

with col2:
    st.metric(
        label="Текущий уровень",
        value=f"{metrics.get('current_level', 1)}",
        delta="2 до следующего"
    )

with col3:
    st.metric(
        label="Место в рейтинге",
        value=f"#{metrics.get('rank_position', 0)}",
        delta="-3 за неделю"
    )

with col4:
    st.metric(
        label="За неделю",
        value=f"{metrics.get('weekly_total', 0)}",
        delta="+12% к прошлой"
    )

# Progress chart
st.markdown("## Прогресс за неделю")

chart_data = prepare_chart_data(user_stats)
if chart_data and 'days' in chart_data and 'points' in chart_data:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=chart_data['days'],
        y=chart_data['points'],
        mode='lines+markers',
        name='Очки',
        line=dict(color='#FF4B4B', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Данные для графика временно недоступны")

# Recent activities
st.markdown("## Последние активности")

try:
    activities = []
    if activities:
        df = format_activity_data(activities[:5])
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Нет недавних активностей")
except:
    st.info("Информация об активностях временно недоступна")

# Activity distribution
st.markdown("## Распределение по типам")

from modules.data_utils import get_activity_distribution
activity_dist = get_activity_distribution(user_stats)

if activity_dist:
    labels = list(activity_dist.keys())
    values = list(activity_dist.values())
    
    fig_pie = px.pie(
        values=values,
        names=labels,
        title='',
        hole=0.4
    )
    fig_pie.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=400
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Sporty Dashboard | Данные обновляются автоматически | Кэш: 5 минут")