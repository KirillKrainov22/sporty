import streamlit as st
from modules.api_client import api
from modules.config import TEST_USER_ID

st.set_page_config(
    page_title="Достижения",
    page_icon="🏆",
    layout="wide",
)

st.title("🏆 Достижения")

user_id = st.sidebar.number_input("User ID", min_value=1, value=TEST_USER_ID, step=1)

with st.spinner("Загружаем достижения..."):
    achievements = api.get_user_achievements(int(user_id))

if not achievements:
    st.warning("Достижения не найдены или пользователь недоступен")
    st.stop()

earned = [a for a in achievements if a.get("earned")]
locked = [a for a in achievements if not a.get("earned")]

st.metric("Получено достижений", f"{len(earned)}/{len(achievements)}")

st.subheader("Полученные")
if earned:
    for ach in earned:
        st.success(f"{ach.get('code')} — {ach.get('title')}")
else:
    st.info("Полученных достижений пока нет")

st.subheader("Недоступные")
if locked:
    for ach in locked:
        st.write(f"🔒 {ach.get('code')} — {ach.get('title')}")
else:
    st.info("Все достижения получены!")

st.sidebar.divider()
st.sidebar.caption("Данные из /api/users/{user_id}/achievements")
