import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Друзья и рейтинги",
    page_icon="👥",
    layout="wide"
)

st.title("👥 Друзья и рейтинги")

# Импортируем API клиент
try:
    from modules.api_client import APIClient
    from modules.charts import create_progress_chart

    @st.cache_resource
    def get_api_client():
        return APIClient(base_url="http://api:8000")
    
    api = get_api_client()

    user_id = st.sidebar.number_input("User ID", min_value=1, value=1, step=1)

    @st.cache_data(ttl=300)
    def get_friends_list(user_id):
        """Получить список друзей"""
        # TODO: Заменить на api.get_friends(user_id)
        return [
            {"id": 2, "username": "alex_sport", "points": 1800, "level": 8},
            {"id": 3, "username": "marina_fit", "points": 2200, "level": 9},
            {"id": 4, "username": "max_runner", "points": 1500, "level": 7},
            {"id": 5, "username": "anna_swimmer", "points": 1950, "level": 8},
            {"id": 6, "username": "dmitry_cyclist", "points": 1700, "level": 7}
        ]
    
    @st.cache_data(ttl=300)
    def get_user_points(user_id):
        """Получить очки текущего пользователя"""
        # TODO: Заменить на реальный API
        return 1250
    
    @st.cache_data(ttl=300)
    def get_friends_comparison(user_id):
        """Сравнение с друзьями"""
        return [
            {"name": "Ты", "points": 1250, "color": "#FF4B4B"},
            {"name": "alex_sport", "points": 1800, "color": "#1F77B4"},
            {"name": "marina_fit", "points": 2200, "color": "#2CA02C"},
            {"name": "max_runner", "points": 1500, "color": "#FF7F0E"},
            {"name": "anna_swimmer", "points": 1950, "color": "#9467BD"}
        ]

    tab1, tab2, tab3 = st.tabs(["📋 Список друзей", "📊 Сравнение", "⚡ Вызовы"])
    
    with tab1:
        st.header("Ваши друзья")
        
        with st.spinner("Загружаем список друзей..."):
            friends = get_friends_list(user_id)
        
        if friends:
            search = st.text_input("Поиск друга по имени")

            filtered_friends = friends
            if search:
                filtered_friends = [f for f in friends if search.lower() in f["username"].lower()]

            for friend in filtered_friends:
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
                    with col1:
                        st.write(f"**{friend['username']}**")
                    with col2:
                        st.write(f"🏆 {friend['points']} очков")
                    with col3:
                        st.write(f"📊 Уровень {friend['level']}")
                    with col4:
                        if st.button("Сравнить", key=f"compare_{friend['id']}"):
                            st.success(f"Сравнение с {friend['username']}")
                            import plotly.graph_objects as go

                            fig = go.Figure()
                            fig.add_trace(go.Bar(
                                x=['Ты', friend['username']],
                                y=[get_user_points(user_id), friend['points']],
                                text=[get_user_points(user_id), friend['points']],
                                textposition='outside',
                                marker_color=['#FF4B4B', '#1F77B4']
                            ))

                            fig.update_layout(
                                title=f"Сравнение с {friend['username']}",
                                showlegend=False,
                                height=300
                            )

                            st.plotly_chart(fig, use_container_width=True)
                    st.divider()
            
            st.metric("Всего друзей", len(friends))
        else:
            st.info("У вас пока нет друзей. Добавьте друзей чтобы соревноваться!")
            
            # Кнопка добавления друга
            if st.button("➕ Найти друзей"):
                st.write("Здесь будет поиск друзей...")
    
    with tab2:
        st.header("Сравнение с друзьями")
        
        # Получаем данные для сравнения
        comparison_data = get_friends_comparison(user_id)
        
        # Столбчатая диаграмма сравнения
        import plotly.graph_objects as go
        
        names = [d["name"] for d in comparison_data]
        points = [d["points"] for d in comparison_data]
        colors = [d["color"] for d in comparison_data]
        
        fig = go.Figure(data=[go.Bar(
            x=names,
            y=points,
            text=points,
            textposition='outside',
            marker_color=colors
        )])
        
        fig.update_layout(
            title="Сравнение очков с друзьями",
            xaxis_title="Пользователь",
            yaxis_title="Очки",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#FAFAFA'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Рейтинг
        st.subheader("Рейтинг среди друзей")
        sorted_friends = sorted(comparison_data, key=lambda x: x["points"], reverse=True)
        
        for i, friend in enumerate(sorted_friends, 1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            st.write(f"{emoji} **{friend['name']}** - {friend['points']} очков")
    
    with tab3:
        st.header("Вызовы друзьям")
        
        st.write("Бросьте вызов другу на недельное соревнование!")
        
        # Выбор друга для вызова
        friends = get_friends_list(user_id)
        if friends:
            friend_options = {f["username"]: f["id"] for f in friends}
            selected_friend = st.selectbox("Выберите друга", list(friend_options.keys()))
            
            # Тип вызова
            challenge_type = st.radio(
                "Тип вызова",
                ["Кто наберет больше очков", "Кто пробежит больше км", "Кто сделает больше тренировок"]
            )
            
            # Длительность
            duration = st.slider("Длительность вызова (дней)", 1, 14, 7)
            
            # Ставка
            stake = st.text_input("Ставка (например, 'обед в кафе')", "гордое звание чемпиона")
            
            if st.button("🎯 Бросить вызов", type="primary"):
                st.success(f"Вызов {selected_friend} брошен! {challenge_type} на {duration} дней. Ставка: {stake}")
        
        # Активные вызовы
        st.subheader("Активные вызовы")
        st.info("Здесь будут отображаться активные вызовы...")
    
    # Футер
    st.sidebar.divider()
    st.sidebar.caption(f"Обновлено: {datetime.now().strftime('%H:%M:%S')}")
    
except ImportError as e:
    st.error(f"Ошибка импорта: {e}")
except Exception as e:
    st.error(f"Ошибка: {e}")
