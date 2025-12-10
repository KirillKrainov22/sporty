import streamlit as st

st.set_page_config(
    page_title="Sporty Dashboard",
    page_icon="🏆",
    layout="wide"
)

st.title("🏆 Sporty Dashboard")
st.write("Главная страница - дашборд")

# Карточки метрик
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Всего очков", "1,250", "+12 сегодня")
with col2:
    st.metric("Текущий уровень", "7", "2 до следующего")
with col3:
    st.metric("Место в рейтинге", "#42", "-3 места")

st.sidebar.success("Выберите страницу из списка выше")
