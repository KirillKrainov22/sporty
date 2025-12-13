import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Админ-панель",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Админ-панель")

# Проверка доступа (пока заглушка)
if "admin_auth" not in st.session_state:
    st.session_state.admin_auth = False

if not st.session_state.admin_auth:
    st.warning("Требуется авторизация администратора")

    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("Логин")
    with col2:
        password = st.text_input("Пароль", type="password")

    if st.button("Войти"):
        if username == "admin" and password == "admin123":  # Заглушка
            st.session_state.admin_auth = True
            st.success("Авторизация успешна!")
            st.rerun()
        else:
            st.error("Неверные учетные данные")
    st.stop()

# Админ авторизован
st.success(f"Администратор: admin | Вход: {datetime.now().strftime('%H:%M:%S')}")
# Вкладки админ-панели
tab1, tab2, tab3, tab4 = st.tabs([
    "👥 Пользователи",
    "📊 Статистика",
    "⚡ Действия",
    "⚙️ Настройки"
])

with tab1:
    st.header("Управление пользователями")

    # Поиск пользователя
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("Поиск по username или telegram_id")
    with col2:
        search_type = st.selectbox("Тип поиска", ["Все", "Активные", "Забаненные"])

    # Тестовые данные пользователей
    users = [
        {"id": 1, "username": "user1", "telegram_id": 12345, "points": 1250, "banned": False},
        {"id": 2, "username": "user2", "telegram_id": 67890, "points": 1800, "banned": False},
        {"id": 3, "username": "user3", "telegram_id": 54321, "points": 900, "banned": True},
        {"id": 4, "username": "user4", "telegram_id": 98765, "points": 2200, "banned": False},
        {"id": 5, "username": "user5", "telegram_id": 13579, "points": 1500, "banned": False}
    ]

    # Фильтрация
    if search_term:
        users = [u for u in users if
                 search_term.lower() in u["username"].lower() or search_term in str(u["telegram_id"])]

    if search_type == "Активные":
        users = [u for u in users if not u["banned"]]
    elif search_type == "Забаненные":
        users = [u for u in users if u["banned"]]

    # Таблица пользователей
    if users:
        st.subheader(f"Найдено пользователей: {len(users)}")

        for user in users:
            with st.expander(f"👤 {user['username']} (ID: {user['id']})"):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.write(f"**Telegram ID:** {user['telegram_id']}")
                with col2:
                    st.write(f"**Очки:** {user['points']}")
                with col3:
                    status = "✅ Активен" if not user['banned'] else "❌ Забанен"
                    st.write(f"**Статус:** {status}")
                with col4:
                    if user['banned']:
                        if st.button("Разбанить", key=f"unban_{user['id']}"):
                            st.success(f"Пользователь {user['username']} разбанен")
                    else:
                        if st.button("Забанить", key=f"ban_{user['id']}"):
                            st.warning(f"Пользователь {user['username']} забанен")

                # Начисление очков
                st.divider()
                st.write("**Ручное управление очками:**")
                col_a, col_b = st.columns([2, 1])
                with col_a:
                    points_change = st.number_input(
                        "Изменение очков",
                        min_value=-1000,
                        max_value=1000,
                        value=100,
                        key=f"points_{user['id']}"
                    )
                with col_b:
                    if st.button("Применить", key=f"apply_{user['id']}"):
                        new_points = user['points'] + points_change
                        st.info(f"Очки пользователя {user['username']}: {user['points']} → {new_points}")
    else:
        st.info("Пользователи не найдены")
        with tab2:
            st.header("Системная статистика")

            # Ключевые метрики
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Всего пользователей", "1,234", "+12 за неделю")
            with col2:
                st.metric("Активных сегодня", "345", "+5")
            with col3:
                st.metric("Всего активностей", "45,678", "+1,234")
            with col4:
                st.metric("Средний чек", "85 очков", "+3")

            st.divider()

            # График активности
            st.subheader("Активность по дням (последние 7 дней)")

            import plotly.graph_objects as go

            days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
            activities = [450, 520, 480, 600, 550, 720, 680]

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=days,
                y=activities,
                text=activities,
                textposition='outside',
                marker_color=['#1F77B4', '#FF7F0E', '#2CA02C', '#D62728', '#9467BD', '#8C564B', '#E377C2']
            ))

            fig.update_layout(
                title="Активность пользователей",
                xaxis_title="День",
                yaxis_title="Количество активностей",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#FAFAFA'
            )

            st.plotly_chart(fig, use_container_width=True)

            # Распределение по активностям
            st.subheader("Популярные активности")

            activity_data = {"Бег": 45, "Велосипед": 25, "Плавание": 15, "Тренировка": 10, "Другое": 5}

            fig2 = go.Figure(data=[go.Pie(
                labels=list(activity_data.keys()),
                values=list(activity_data.values()),
                textinfo='label+percent'
            )])

            fig2.update_layout(
                title="Распределение по типам активностей",
                showlegend=False
            )

            st.plotly_chart(fig2, use_container_width=True)
            with tab3:
                st.header("Быстрые действия")

                st.write("Массовые операции и утилиты")

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Массовые операции")

                    operation = st.selectbox(
                        "Выберите операцию",
                        ["Начислить очки всем", "Сбросить пароли", "Отправить уведомление"]
                    )

                    if operation == "Начислить очки всем":
                        bonus_points = st.number_input("Бонусные очки", min_value=1, max_value=1000, value=50)
                        if st.button("Начислить всем", type="primary"):
                            st.success(f"Начислено {bonus_points} очков всем активным пользователям")

                    elif operation == "Сбросить пароли":
                        st.warning("Будет отправлена ссылка для сброса пароля всем пользователям")
                        if st.button("Отправить ссылки"):
                            st.info("Ссылки для сброса отправлены на email пользователей")

                    elif operation == "Отправить уведомление":
                        message = st.text_area("Сообщение для пользователей")
                        if st.button("Отправить уведомление"):
                            st.success("Уведомление отправлено всем пользователям")

                with col2:
                    st.subheader("Системные утилиты")

                    if st.button("Очистить кэш API"):
                        st.session_state.clear()
                        st.success("Кэш очищен")

                    if st.button("Проверить соединение с БД"):
                        st.success("Соединение с базой данных: OK")

                    if st.button("Экспорт статистики"):
                        st.info("Статистика экспортирована в CSV файл")

                    if st.button("Резервное копирование"):
                        st.info("Резервная копия создана")

            with tab4:
                st.header("Настройки системы")

                st.subheader("Параметры системы")

                col1, col2 = st.columns(2)

                with col1:
                    points_per_km = st.number_input("Очков за 1 км бега", min_value=1, max_value=50, value=10)
                    points_per_swim = st.number_input("Очков за 1 км плавания", min_value=1, max_value=50, value=15)
                    morning_bonus = st.slider("Утренний бонус (%)", 0, 200, 100)

                with col2:
                    weekend_bonus = st.slider("Выходной бонус (%)", 0, 200, 150)
                    min_level_points = st.number_input("Очков для 1 уровня", min_value=100, max_value=5000, value=1000)
                    points_per_level = st.number_input("Очков за каждый след. уровень", min_value=100, max_value=5000,
                                                       value=500)

                if st.button("Сохранить настройки", type="primary"):
                    st.success("Настройки сохранены!")

                st.divider()

                st.subheader("Опасная зона")

                if st.button("🔄 Пересчитать все очки", type="secondary"):
                    st.warning("Пересчет всех очков может занять несколько минут")

                if st.button("🗑️ Удалить неактивных пользователей", type="secondary"):
                    st.error("Будут удалены пользователи без активности более 90 дней")
                    confirm = st.checkbox("Я подтверждаю удаление")
                    if confirm and st.button("Подтвердить удаление", type="primary"):
                        st.error("Удалено 23 неактивных пользователя")

            st.sidebar.divider()
            st.sidebar.write("**Версия системы:** 1.0.0")
            st.sidebar.write(f"**Последнее обновление:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            if st.sidebar.button("Выйти из админки"):
                st.session_state.admin_auth = False
                st.rerun()