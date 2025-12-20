# modules/charts.py (окончательная версия БЕЗ pandas)
import plotly.graph_objects as go
from typing import List, Dict


def create_progress_chart(data: List[Dict], title: str = "Прогресс по дням") -> go.Figure:
    """Линейный график прогресса - не требует pandas"""
    if not data:
        fig = go.Figure()
        fig.update_layout(title=title)
        return fig

    dates = [item.get('date', '') for item in data]
    points = [item.get('points', 0) for item in data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=points,
        mode='lines+markers',
        name='Очки',
        line=dict(color='#FF4B4B', width=3),
        marker=dict(size=8)
    ))

    fig.update_layout(
        title=title,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#FAFAFA',
        xaxis_title="Дата",
        yaxis_title="Очки",
        hovermode='x unified'
    )

    return fig


def create_activity_distribution_chart(data: Dict, title: str = "Распределение активностей") -> go.Figure:
    """Круговая диаграмма - не требует pandas"""
    if not data:
        fig = go.Figure()
        fig.update_layout(title=title)
        return fig

    labels = list(data.keys())
    values = list(data.values())

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        textinfo='label+percent',
        insidetextorientation='radial'
    )])

    fig.update_layout(
        title=title,
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#FAFAFA'
    )

    return fig


def create_weekly_comparison_chart(data: List[Dict], title: str = "Сравнение по неделям") -> go.Figure:
    """Столбчатая диаграмма - не требует pandas"""
    if not data:
        fig = go.Figure()
        fig.update_layout(title=title)
        return fig

    weeks = [item.get('week', '') for item in data]
    points = [item.get('total_points', 0) for item in data]

    fig = go.Figure(data=[go.Bar(
        x=weeks,
        y=points,
        text=points,
        textposition='outside',
        marker_color='#1F77B4'
    )])

    fig.update_layout(
        title=title,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#FAFAFA',
        xaxis_title="Неделя",
        yaxis_title="Всего очков"
    )

    return fig
