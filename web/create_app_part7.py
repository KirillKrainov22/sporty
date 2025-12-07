with open('app.py', 'a', encoding='utf-8') as f:
    f.write("""

# Footer
st.markdown("---")
st.caption("Sporty Dashboard | Данные обновляются автоматически | Кэш: 5 минут")""")
