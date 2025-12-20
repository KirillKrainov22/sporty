import streamlit as st
from datetime import datetime
import plotly.graph_objects as go

st.set_page_config(
    page_title="Друзья",
    page_icon="👥",
    layout="wide"
)

st.title("👥 Друзья и рейтинги")

st.info(
    "🏆 Локальный режим\n\n"
    "Используются тестовые данные. "
    "Страница готова к подключению реального API."
)


USER_ID = 1

FRIENDS = [
    {"id": 2, "username": "alex_sport", "points": 1800, "level": 8},
    {"id": 3, "username": "marina_fit", "points": 2200, "level": 9},
    {"id": 4, "username": "max_runner", "points": 1500, "level": 7},
    {"id": 5, "username": "anna_swimmer", "points": 1950, "level": 8},
]

MY_POINTS = 1250

tab1, tab2, tab3 = st.tabs([
    "👥 Список друзей",
    "⚖️ Сравнение",
    "⚔️ Вызовы"
])


with tab1:
    st.subheader("Ваши друзья")

    search = st.text_input("Поиск по имени")

    filtered = FRIENDS
    if search:
        filtered = [
            f for f in FRIENDS
            if search.lower() in f["username"].lower()
        ]

    if not filtered:
        st.info("Друзья не найдены")
    else:
        for friend in filtered:
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

                col1.write(f"**{friend['username']}**")
                col2.write(f"⭐ {friend['points']} очков")
                col3.write(f"⭐ Уровень {friend['level']}")

                with col4:
                    if st.button(
                        "Сравнить",
                        key=f"compare_{friend['id']}"
                    ):
                        fig = go.Figure()

                        fig.add_trace(go.Bar(
                            x=["Ты", friend["username"]],
                            y=[MY_POINTS, friend["points"]],
                            text=[MY_POINTS, friend["points"]],
                            textposition="outside",
                            marker_color=["#FF4B4B", "#1F77B4"]
                        ))

                        fig.update_layout(
                            title=f"Сравнение с {friend['username']}",
                            showlegend=False,
                            height=300
                        )

                        st.plotly_chart(
                            fig,
                            use_container_width=True
                        )

                st.divider()

        st.metric("Всего друзей", len(FRIENDS))


with tab2:
    st.subheader("Сравнение очков")

    comparison = [
        {"name": "Ты", "points": MY_POINTS},
        *[
            {"name": f["username"], "points": f["points"]}
            for f in FRIENDS
        ]
    ]

    names = [u["name"] for u in comparison]
    points = [u["points"] for u in comparison]

    fig = go.Figure(
        data=[go.Bar(
            x=names,
            y=points,
            text=points,
            textposition="outside"
        )]
    )

    fig.update_layout(
        title="Очки среди друзей",
        xaxis_title="Пользователь",
        yaxis_title="Очки",
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Рейтинг")

    sorted_users = sorted(
        comparison,
        key=lambda x: x["points"],
        reverse=True
    )

    for i, user in enumerate(sorted_users, 1):
        medal = "??" if i == 1 else "??" if i == 2 else "??" if i == 3 else f"{i}."
        st.write(f"{medal} **{user['name']}** — {user['points']} очков")

with tab3:
    st.subheader("Вызов другу")

    friend_names = [f["username"] for f in FRIENDS]
    selected_friend = st.selectbox(
        "Выберите друга",
        friend_names
    )

    challenge_type = st.radio(
        "Тип вызова",
        [
            "Кто наберёт больше очков",
            "Кто пробежит больше км",
            "Кто сделает больше тренировок"
        ]
    )

    duration = st.slider(
        "Длительность (дней)",
        1, 14, 7
    )

    stake = st.text_input(
        "Ставка",
        "гордое звание чемпиона"
    )

    if st.button("🥊 Бросить вызов", type="primary"):
        st.success(
            f"Вызов брошен!\n\n"
            f"Друг: **{selected_friend}**\n"
            f"Тип: **{challenge_type}**\n"
            f"Длительность: **{duration} дней**\n"
            f"Ставка: **{stake}**"
        )


st.sidebar.divider()
st.sidebar.caption(
    f"Обновлено: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)
