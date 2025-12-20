import streamlit as st

st.set_page_config(
    page_title="Достижения",
    page_icon="🏆",
    layout="wide"
)

st.title("🏆 Достижения")

try:
    from modules.api_client import APIClient
    
    @st.cache_resource
    def get_api_client():
        return APIClient(base_url="http://api:8000")
    
    api = get_api_client()
    user_id = st.sidebar.number_input("User ID", min_value=1, value=1, step=1)

    ALL_ACHIEVEMENTS = {
        "first_activity": {
            "name": "Первый забег",
            "description": "Завершить первую тренировку",
            "icon": "🏃",
            "points": 50,
            "condition": "activities_count >= 1"
        },
        "consistent_week": {
            "name": "Стабильный",
            "description": "7 дней подряд с тренировками",
            "icon": "🔥",
            "points": 100,
            "condition": "streak_days >= 7"
        },
        "marathoner": {
            "name": "Марафонец",
            "description": "Пробежать 100 км за месяц",
            "icon": "🏅",
            "points": 200,
            "condition": "monthly_distance >= 100"
        },
        "social_butterfly": {
            "name": "Социальная бабочка",
            "description": "Добавить 10 друзей",
            "icon": "🦋",
            "points": 150,
            "condition": "friends_count >= 10"
        },
        "champion": {
            "name": "Чемпион",
            "description": "Выиграть 5 вызовов",
            "icon": "🥇",
            "points": 300,
            "condition": "challenges_won >= 5"
        },
        "early_bird": {
            "name": "Ранняя пташка",
            "description": "5 тренировок до 7 утра",
            "icon": "🐦",
            "points": 75,
            "condition": "morning_activities >= 5"
        },
        "weekend_warrior": {
            "name": "Воин выходного дня",
            "description": "10 тренировок в выходные",
            "icon": "⚔️",
            "points": 80,
            "condition": "weekend_activities >= 10"
        },
        "record_breaker": {
            "name": "Рекордсмен",
            "description": "Побить личный рекорд 3 раза",
            "icon": "💪",
            "points": 250,
            "condition": "records_broken >= 3"
        }
    }

    @st.cache_data(ttl=300)
    def get_user_achievements(user_id):
        """Получить достижения пользователя"""
        # TODO: Заменить на api.get_achievements(user_id)
        return {
            "earned": ["first_activity", "consistent_week", "early_bird"],
            "stats": {
                "activities_count": 15,
                "streak_days": 7,
                "monthly_distance": 85,
                "friends_count": 8,
                "challenges_won": 3,
                "morning_activities": 5,
                "weekend_activities": 7,
                "records_broken": 2
            }
        }

    st.header("Ваши достижения")

    with st.spinner("Загружаем достижения..."):
        user_data = get_user_achievements(user_id)
    
    earned_achievements = user_data["earned"]
    user_stats = user_data["stats"]

    progress = len(earned_achievements) / len(ALL_ACHIEVEMENTS) * 100
    st.metric("Всего достижений", f"{len(earned_achievements)}/{len(ALL_ACHIEVEMENTS)}", f"{progress:.1f}%")

    st.subheader("Заработанные достижения")

    cols = st.columns(3)
    
    for i, (achievement_id, achievement) in enumerate(ALL_ACHIEVEMENTS.items()):
        col = cols[i % 3]
        
        with col:
            if achievement_id in earned_achievements:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 15px;
                    border-radius: 10px;
                    text-align: center;
                    margin-bottom: 10px;
                ">
                    <div style="font-size: 2em;">{achievement['icon']}</div>
                    <div style="font-weight: bold; font-size: 1.1em;">{achievement['name']}</div>
                    <div style="font-size: 0.9em; opacity: 0.9;">{achievement['description']}</div>
                    <div style="font-size: 0.8em; margin-top: 5px;">+{achievement['points']} очков</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="
                    background: #262730;
                    padding: 15px;
                    border-radius: 10px;
                    text-align: center;
                    margin-bottom: 10px;
                    opacity: 0.7;
                ">
                    <div style="font-size: 2em; filter: grayscale(100%);">{achievement['icon']}</div>
                    <div style="font-weight: bold; font-size: 1.1em;">???</div>
                    <div style="font-size: 0.9em; opacity: 0.9;">Скрытое достижение</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.header("Ближайшие цели")
    
    upcoming_achievements = []
    
    for achievement_id, achievement in ALL_ACHIEVEMENTS.items():
        if achievement_id not in earned_achievements:
            condition = achievement["condition"]
            upcoming_achievements.append({
                "id": achievement_id,
                **achievement,
                "progress": 0.6
            })
    
    for achievement in upcoming_achievements[:3]:
        st.write(f"**{achievement['icon']} {achievement['name']}**")
        st.write(f"{achievement['description']}")
        
        progress_value = achievement["progress"]
        st.progress(progress_value)
        
        if achievement["id"] == "marathoner":
            st.caption(f"Пробежано: {user_stats['monthly_distance']}/100 км")
        elif achievement["id"] == "social_butterfly":
            st.caption(f"Друзей: {user_stats['friends_count']}/10")
        elif achievement["id"] == "champion":
            st.caption(f"Побед в вызовах: {user_stats['challenges_won']}/5")
        
        st.divider()
    
    st.sidebar.divider()
    st.sidebar.subheader("Статистика")
    st.sidebar.write(f"⏱️ Всего активностей: {user_stats['activities_count']}")
    st.sidebar.write(f"📅 Серия дней: {user_stats['streak_days']}")
    st.sidebar.write(f"👥 Друзей: {user_stats['friends_count']}")
    st.sidebar.write(f"🏆 Побито рекордов: {user_stats['records_broken']}")
    
except ImportError as e:
    st.error(f"Ошибка импорта: {e}")
except Exception as e:
    st.error(f"Ошибка: {e}")
