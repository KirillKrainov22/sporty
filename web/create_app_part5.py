with open('app.py', 'a', encoding='utf-8') as f:
    f.write("""

# Progress chart
st.markdown("## Прогресс за неделю")

chart_data = prepare_chart_data(user_stats)
if chart_data and 'days' in chart_data and 'points' in chart_data:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=chart_data['days'],
        y=chart_data['points'],
        mode='lines+markers',
        name='Очки',
        line=dict(color='#FF4B4B', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Данные для графика временно недоступны")""")
