"""
Data processing utilities for Sporty Dashboard
"""
import pandas as pd
from typing import Dict, List, Any


def prepare_chart_data(stats_data: Dict) -> Dict[str, List]:
    """Prepare weekly progress data for Plotly chart"""
    if not stats_data:
        return {"days": [], "points": []}
    
    weekly = stats_data.get('weekly_progress', [])
    if not weekly:
        return {"days": [], "points": []}
    
    return {
        "days": [item.get('day', '') for item in weekly],
        "points": [item.get('points', 0) for item in weekly]
    }

def format_activity_data(activities: List[Dict]) -> pd.DataFrame:
    """Format activities for display in DataFrame"""
    if not activities:
        return pd.DataFrame()
    
    data = []
    for act in activities:
        data.append({
            "Тип": act.get('type', 'Неизвестно'),
            "Дистанция": f"{act.get('distance', 0)} км",
            "Очки": act.get('points', 0),
            "Время": act.get('time', '')
        })
    
    return pd.DataFrame(data)

def calculate_metrics(stats_data: Dict) -> Dict[str, Any]:
    """Calculate derived metrics from user stats"""
    if not stats_data:
        return {}
    
    weekly = stats_data.get('weekly_progress', [])
    total_weekly = sum(item.get('points', 0) for item in weekly) if weekly else 0
    
    return {
        "total_points": stats_data.get('total_points', 0),
        "current_level": stats_data.get('current_level', 1),
        "rank_position": stats_data.get('rank_position', 0),
        "weekly_total": total_weekly,
        "daily_average": round(total_weekly / 7, 1) if weekly else 0
    }

def get_activity_distribution(stats_data: Dict) -> Dict[str, float]:
    """Extract activity distribution for pie chart"""
    if not stats_data:
        return {}
    
    distribution = stats_data.get('activity_distribution', {})
    if not distribution:
        distribution = {
            "Бег": 35,
            "Велосипед": 25,
            "Плавание": 20,
            "Зал": 15,
            "Йога": 5
        }
    
    return distribution
