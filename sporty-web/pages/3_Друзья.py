import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from modules.api_client import api
from modules.config import TEST_USER_ID

st.set_page_config(
    page_title="Друзья",
    page_icon="👥",
    layout="wide",
)

st.title("👥 Друзья и рейтинги")

user_id = st.sidebar.number_input("Ваш user_id", min_value=1, value=TEST_USER_ID, step=1)

col_info, col_action = st.columns([2, 1])
with col_action:
    st.subheader("Добавить друга")
    friend_id = st.number_input("ID друга", min_value=1, step=1)
    if st.button("➕ Добавить", type="primary"):
        with st.spinner("Отправляем запрос..."):
            response = api.add_friend(user_id=int(user_id), friend_id=int(friend_id))
        if response:
            st.success("Друг добавлен или уже в списке")
        else:
            st.error("Не удалось добавить друга. Проверьте ID и статус пользователя")

with col_info:
    st.subheader("Список друзей")
    with st.spinner("Загружаем друзей..."):
        friends = api.get_user_friends(int(user_id))

    if not friends:
        st.info("Список друзей пуст")
    else:
        for friend in friends:
            st.write(
                f"ID связи: {friend.get('id')} • user_id: {friend.get('user_id')} "
                f"↔ friend_id: {friend.get('friend_id')} • статус: {friend.get('status')}"
            )
        st.metric("Всего друзей", len(friends))

st.divider()

st.subheader("Рейтинг среди друзей")
with st.spinner("Получаем рейтинг..."):
    lb = api.get_friends_leaderboard(int(user_id))

if lb:
    names = [str(item.get("username") or item.get("user_id")) for item in lb]
    points = [item.get("points", 0) for item in lb]
    fig = go.Figure(data=[go.Bar(x=names, y=points, text=points, textposition="outside")])
    fig.update_layout(height=420, yaxis_title="Очки")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Нет данных для рейтинга среди друзей")

st.sidebar.divider()
st.sidebar.caption(f"Обновлено: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
