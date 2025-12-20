import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta

USE_API = False

st.set_page_config(
    page_title="Детальная статистика",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Детальная статистика пользователя")


def get_mock_user_stats(days=30):
    data = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=days - i)).strftime("%Y-%m-%d")
        points = 80 + (i % 7) * 15 + i * 3
        data.append({"date": date, "points": points})
    return data


user_id = st.sidebar.number_input("User ID", min_value=1, value=1, step=1)

with st.spinner("Загружаем данные..."):
    if USE_API:
        try:
            from modules.api_client import api
            stats = api.get_user_stats(user_id)
            if not stats:
                raise ValueError("API вернул пустые данные")
            progress_data = stats["daily_progress"]
        except Exception as e:
            st.error("Ошибка при загрузке данных из API")
            st.stop()
    else:
        progress_data = get_mock_user_stats(30)


st.subheader("📈 Прогресс по дням")

dates = [d["date"] for d in progress_data]
points = [d["points"] for d in progress_data]

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=dates,
    y=points,
    mode="lines+markers",
    name="Очки"
))

fig.update_layout(
    xaxis_title="Дата",
    yaxis_title="Очки",
    height=400
)

st.plotly_chart(fig, use_container_width=True)


st.subheader("📌 Ключевые показатели")

col1, col2, col3 = st.columns(3)

col1.metric("Всего очков", sum(points))
col2.metric("Среднее в день", sum(points) // len(points))
col3.metric("Максимум за день", max(points))


st.divider()

if USE_API:
    st.success("Данные получены из backend API")
else:
    st.info(
        "🔧 Локальный режим\n\n"
        "Используются тестовые данные. "
    )

st.caption(f"Обновлено: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
