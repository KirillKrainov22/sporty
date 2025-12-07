with open('app.py', 'a', encoding='utf-8') as f:
    f.write("""

# Metrics cards
st.markdown("## Основные показатели")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Всего очков",
        value=f"{metrics.get('total_points', 0):,}",
        delta=f"+{metrics.get('daily_average', 0):.0f} в день"
    )

with col2:
    st.metric(
        label="Текущий уровень",
        value=f"{metrics.get('current_level', 1)}",
        delta="2 до следующего"
    )

with col3:
    st.metric(
        label="Место в рейтинге",
        value=f"#{metrics.get('rank_position', 0)}",
        delta="-3 за неделю"
    )

with col4:
    st.metric(
        label="За неделю",
        value=f"{metrics.get('weekly_total', 0)}",
        delta="+12% к прошлой"
    )""")
