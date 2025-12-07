with open('app.py', 'w', encoding='utf-8') as f:
    f.write("""import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Our modules
from modules.api_client import api
from modules.cache import cache
from modules.mock_data import MOCK_DATA
from modules.data_utils import prepare_chart_data, calculate_metrics, format_activity_data

# Page config
st.set_page_config(
    page_title="Sporty Dashboard",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Sporty Dashboard")
st.markdown("### Статистика активности")""")
