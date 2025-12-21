import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from modules.api_client import api
from modules.config import TEST_USER_ID

st.set_page_config(
    page_title="Детальная статистика",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Детальная статистика пользователя")

user_id = st.sidebar.number_input("User ID", min_value=1, value=TEST_USER_ID, step=1)

with st.spinner("Загружаем данные..."):
    stats = api.get_user_stats(user_id)

if not stats:
    st.error("Не удалось получить статистику пользователя из API")
    st.stop()

st.subheader("📈 Прогресс по дням")

progress_data = stats.get("daily_progress", [])
dates = [d.get("date") for d in progress_data]
points = [d.get("points", 0) for d in progress_data]

if dates and points:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=points,
            mode="lines+markers",
            name="Очки",
        )
    )
    fig.update_layout(xaxis_title="Дата", yaxis_title="Очки", height=400)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Нет данных о ежедневном прогрессе")

st.subheader("📊 Ключевые показатели")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Всего очков", stats.get("points", 0))
col2.metric("Уровень", stats.get("level", 0))
col3.metric("Всего активностей", stats.get("total_activities", 0))
col4.metric("Глобальный ранг", stats.get("global_rank", "—"))

st.divider()

st.subheader("Статистика по активностям")
activity_stats = stats.get("activity_type_stats", [])
if activity_stats:
    labels = [item.get("type", "unknown") for item in activity_stats]
    values = [item.get("count", 0) for item in activity_stats]
    pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
    pie.update_layout(height=360)
    st.plotly_chart(pie, use_container_width=True)
else:
    st.info("Нет статистики по типам активностей")

st.divider()
st.success("Данные получены из backend API")
st.caption(f"Обновлено: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
