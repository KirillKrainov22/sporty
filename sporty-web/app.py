import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Sporty — платформа геймификации спорта",
    page_icon="🏆",
    layout="wide"
)

st.title("🏆 Sporty")
st.subheader("Платформа геймификации спорта и активности")

st.markdown(
    """
    **Sporty** — это учебный проект, демонстрирующий, как можно
    мотивировать пользователей заниматься спортом с помощью очков,
    уровней, соревнований и рейтингов.
    """
)

st.divider()

st.header("🚀 Возможности платформы")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 👤 Пользователь")
    st.write(
        """
        - Регистрация по Telegram ID  
        - Очки и уровни  
        - Персональная статистика  
        """
    )

with col2:
    st.markdown("### 📊 Статистика")
    st.write(
        """
        - Прогресс по дням  
        - Аналитика активности  
        - Визуализация данных  
        """
    )

with col3:
    st.markdown("### 👥 Социальные функции")
    st.write(
        """
        - Друзья  
        - Сравнение результатов  
        - Соревнования  
        """
    )

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("### 🎯 Челленджи")
    st.write(
        """
        - Вызовы между пользователями  
        - Разные типы соревнований  
        """
    )

with col5:
    st.markdown("### 🏆 Лидерборды")
    st.write(
        """
        - Глобальный рейтинг  
        - Рейтинг среди друзей  
        """
    )

with col6:
    st.markdown("### ⚙️ Админ-панель")
    st.write(
        """
        - Управление пользователями  
        - Бан / разбан  
        - Начисление очков  
        - Общая статистика системы  
        """
    )

st.divider()


st.info(
    "🔧 Сейчас приложение запущено в **локальном демонстрационном режиме** "
    "с тестовыми данными."
)

st.divider()

st.caption(
    f"Sporty • Учебный проект • {datetime.now().strftime('%Y-%m-%d %H:%M')}"
)
