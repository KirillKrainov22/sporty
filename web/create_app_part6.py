with open('app.py', 'a', encoding='utf-8') as f:
    f.write("""

# Recent activities
st.markdown("## Последние активности")

try:
    activities = []
    if activities:
        df = format_activity_data(activities[:5])
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Нет недавних активностей")
except:
    st.info("Информация об активностях временно недоступна")

# Activity distribution
st.markdown("## Распределение по типам")

from modules.data_utils import get_activity_distribution
activity_dist = get_activity_distribution(user_stats)

if activity_dist:
    labels = list(activity_dist.keys())
    values = list(activity_dist.values())
    
    fig_pie = px.pie(
        values=values,
        names=labels,
        title='',
        hole=0.4
    )
    fig_pie.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=400
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)""")
