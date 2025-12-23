import streamlit as st
from datetime import datetime
from modules.api_client import api
from modules.config import ADMIN_TOKEN as DEFAULT_ADMIN_TOKEN

st.set_page_config(
    page_title="Админка",
    page_icon="⚙️",
    layout="wide",
)

st.title("⚙️ Административная панель")

admin_token = st.sidebar.text_input(
    "X-Admin-Token",
    value=DEFAULT_ADMIN_TOKEN,
    type="password",
    help="Токен обязателен для /api/admin/*",
)

if not admin_token:
    st.warning("Укажите X-Admin-Token для запросов к админке")
    st.stop()

@st.cache_data(ttl=30)
def load_admin_data(token: str):
    users = api.get_admin_users(token) or []
    stats = api.get_admin_statistics(token) or {}
    return users, stats

with st.spinner("Загружаем данные админки..."):
    users, system_stats = load_admin_data(admin_token)

if not users:
    st.warning("Список пользователей пуст или токен неверен")

if not system_stats:
    st.info("Не удалось получить системную статистику")

users_tab, stats_tab, actions_tab = st.tabs([
    "👥 Пользователи",
    "📊 Статистика",
    "🚀 Действия",
])

with users_tab:
    st.subheader("Управление пользователями")
    search = st.text_input("Поиск по username или telegram_id")

    filtered = users
    if search:
        filtered = [
            u
            for u in users
            if search.lower() in str(u.get("username", "")).lower()
            or search in str(u.get("telegram_id", ""))
        ]

    if not filtered:
        st.info("Пользователи не найдены")
    else:
        for user in filtered:
            with st.expander(f"{user.get('username') or '—'} (ID {user.get('id')})"):
                col1, col2, col3, col4 = st.columns(4)
                col1.write(f"Telegram ID: {user.get('telegram_id')}")
                col2.write(f"Очки: {user.get('points')}")
                col3.write(f"Уровень: {user.get('level')}")
                status = "🚫 Забанен" if user.get("is_banned") else "✅ Активен"
                col4.write(status)

                new_status = not user.get("is_banned")
                if st.button(
                    "Разбанить" if user.get("is_banned") else "Забанить",
                    key=f"ban_{user['id']}",
                ):
                    result = api.ban_user(user_id=user["id"], is_banned=new_status, admin_token=admin_token)
                    if result:
                        st.success("Статус обновлён")
                        load_admin_data.clear()
                    else:
                        st.error("Не удалось изменить статус")

                delta = st.number_input(
                    "Изменение очков", -1000, 1000, 0, key=f"points_{user['id']}"
                )
                if st.button("Применить", key=f"apply_{user['id']}"):
                    res = api.update_user_points(
                        user_id=user["id"], amount=int(delta), admin_token=admin_token
                    )
                    if res:
                        st.success("Очки обновлены")
                        load_admin_data.clear()
                    else:
                        st.error("Не удалось обновить очки")

with stats_tab:
    st.subheader("Системная статистика")
    if system_stats:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Всего пользователей", system_stats.get("total_users", 0))
        col2.metric("Активных сегодня", system_stats.get("active_users_today", 0))
        col3.metric("Всего активностей", system_stats.get("total_activities", 0))
        col4.metric("Всего очков", system_stats.get("total_points", 0))

        st.divider()
        st.subheader("Активности по типам")
        activities_by_type = system_stats.get("activities_by_type", {})
        if activities_by_type:
            labels = list(activities_by_type.keys())
            values = list(activities_by_type.values())
            import plotly.graph_objects as go

            pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
            pie.update_layout(height=400)
            st.plotly_chart(pie, use_container_width=True)
        else:
            st.info("Нет данных по активностям")

        st.divider()
        st.subheader("🏆 Топ пользователей")
        for i, user in enumerate(system_stats.get("top_users", []), 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            st.write(
                f"{medal} {user.get('username', '—')} — {user.get('points', 0)} очков"
            )
    else:
        st.warning("Данные не получены")

with actions_tab:
    st.subheader("Сервисные операции")
    st.info("Доступные действия ограничены контрактом API: бан, изменение очков, статистика.")

st.sidebar.divider()
st.sidebar.caption(
    f"Администратор | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)
