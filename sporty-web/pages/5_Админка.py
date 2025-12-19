import streamlit as st
from datetime import datetime
import plotly.graph_objects as go

st.set_page_config(
    page_title="Админка",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Административная панель")

st.info(
    "🔧 Локальный режим\n\n"
    "Админка работает на тестовых данных. "
    "Готова к подключению backend API."
)

USERS = [
    {
        "id": 1,
        "telegram_id": 1001,
        "username": "kirill",
        "points": 1250,
        "level": 7,
        "is_banned": False
    },
    {
        "id": 2,
        "telegram_id": 1002,
        "username": "alex",
        "points": 1800,
        "level": 8,
        "is_banned": False
    },
    {
        "id": 3,
        "telegram_id": 1003,
        "username": "marina",
        "points": 2200,
        "level": 9,
        "is_banned": True
    },
]

SYSTEM_STATS = {
    "total_users": 5,
    "active_users_today": 3,
    "total_activities": 42,
    "total_points": 6400,
    "activities_by_type": {
        "run": 18,
        "walk": 10,
        "bike": 8,
        "swim": 6
    },
    "top_users": [
        {"username": "marina", "points": 2200},
        {"username": "alex", "points": 1800},
        {"username": "kirill", "points": 1250},
    ]
}

tab1, tab2, tab3 = st.tabs([
    "👥 Пользователи",
    "📊 Статистика",
    "⚡ Действия"
])

with tab1:
    st.subheader("Управление пользователями")

    search = st.text_input("Поиск по username или telegram_id")

    filtered_users = USERS
    if search:
        filtered_users = [
            u for u in USERS
            if search.lower() in u["username"].lower()
            or search in str(u["telegram_id"])
        ]

    if not filtered_users:
        st.info("Пользователи не найдены")
    else:
        for user in filtered_users:
            with st.expander(f"👤 {user['username']} (ID {user['id']})"):
                col1, col2, col3, col4 = st.columns(4)

                col1.write(f"Telegram ID: {user['telegram_id']}")
                col2.write(f"Очки: {user['points']}")
                col3.write(f"Уровень: {user['level']}")

                status = "❌ Забанен" if user["is_banned"] else "✅ Активен"
                col4.write(status)

                if user["is_banned"]:
                    if st.button("Разбанить", key=f"unban_{user['id']}"):
                        st.success("Пользователь разбанен (локально)")
                else:
                    if st.button("Забанить", key=f"ban_{user['id']}"):
                        st.warning("Пользователь забанен (локально)")

                st.divider()

                delta = st.number_input(
                    "Изменение очков",
                    -1000,
                    1000,
                    50,
                    key=f"points_{user['id']}"
                )

                if st.button("Применить", key=f"apply_{user['id']}"):
                    st.success(
                        f"Очки изменены: {user['points']} → {user['points'] + delta}"
                    )


with tab2:
    st.subheader("Системная статистика")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Всего пользователей", SYSTEM_STATS["total_users"])
    col2.metric("Активных сегодня", SYSTEM_STATS["active_users_today"])
    col3.metric("Всего активностей", SYSTEM_STATS["total_activities"])
    col4.metric("Всего очков", SYSTEM_STATS["total_points"])

    st.divider()

    st.subheader("Активности по типам")

    fig = go.Figure(
        data=[go.Pie(
            labels=list(SYSTEM_STATS["activities_by_type"].keys()),
            values=list(SYSTEM_STATS["activities_by_type"].values()),
            hole=0.4
        )]
    )

    fig.update_layout(
        title="Распределение активностей",
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("🏆 Топ пользователей")

    for i, user in enumerate(SYSTEM_STATS["top_users"], 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
        st.write(f"{medal} **{user['username']}** — {user['points']} очков")


with tab3:
    st.subheader("Административные действия")

    operation = st.selectbox(
        "Выберите действие",
        [
            "Начислить очки всем",
            "Отправить уведомление",
            "Очистить кэш"
        ]
    )

    if operation == "Начислить очки всем":
        bonus = st.number_input("Количество очков", 1, 1000, 50)
        if st.button("Начислить"):
            st.success(f"Начислено {bonus} очков всем пользователям (локально)")

    elif operation == "Отправить уведомление":
        message = st.text_area("Текст уведомления")
        if st.button("Отправить"):
            st.success("Уведомление отправлено (локально)")

    elif operation == "Очистить кэш":
        if st.button("Очистить"):
            st.success("Кэш очищен (локально)")

st.sidebar.divider()
st.sidebar.caption(
    f"Администратор | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)


