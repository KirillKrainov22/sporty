"""
Mock data for development
"""

def get_mock_user_stats(user_id=1):
    return {
        "total_points": 1250,
        "current_level": 7,
        "rank_position": 42,
        "weekly_progress": [
            {"day": "Mon", "points": 120},
            {"day": "Tue", "points": 150},
            {"day": "Wed", "points": 200},
            {"day": "Thu", "points": 180},
            {"day": "Fri", "points": 250},
            {"day": "Sat", "points": 300},
            {"day": "Sun", "points": 50}
        ]
    }

MOCK_DATA = {
    "user_stats": get_mock_user_stats
}
