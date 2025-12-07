with open('app.py', 'a', encoding='utf-8') as f:
    f.write("""

# Sidebar
with st.sidebar:
    st.markdown("### Настройки")
    
    user_id = st.number_input("ID пользователя", min_value=1, value=1)
    
    st.markdown("---")
    st.markdown("### Управление кэшем")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Обновить данные", type="primary"):
            cache.clear()
            st.rerun()
    
    with col2:
        if st.button("Очистить кэш API"):
            api.clear_cache()
            st.rerun()""")
