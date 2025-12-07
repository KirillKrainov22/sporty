import sys
sys.path.insert(0, '.')

print("=== Full Workflow Test (No Emoji) ===")

# 1. Test imports
try:
    from modules.api_client import api
    from modules.cache import cache, cached
    from modules.data_utils import prepare_chart_data
    from modules.mock_data import MOCK_DATA
    print("PASS 1. All imports work")
except Exception as e:
    print(f"FAIL 1. Import error: {e}")
    sys.exit(1)

# 2. Test API client methods
print("\n2. Testing API methods...")
methods = ['get_user_stats', 'clear_cache']
for method in methods:
    if hasattr(api, method):
        print(f"   PASS {method} exists")
    else:
        print(f"   FAIL {method} missing")

# 3. Test mock data
print("\n3. Testing mock data...")
try:
    mock_stats = MOCK_DATA["user_stats"](1)
    if isinstance(mock_stats, dict):
        print(f"   PASS Mock data: {mock_stats.get('total_points', 'N/A')} points")
    else:
        print("   FAIL Mock data not a dict")
except Exception as e:
    print(f"   FAIL Mock data error: {e}")

# 4. Test data utils
print("\n4. Testing data utils...")
try:
    test_data = {'weekly_progress': [{'day': 'Mon', 'points': 100}]}
    chart_data = prepare_chart_data(test_data)
    if isinstance(chart_data, dict):
        print(f"   PASS Data utils work")
    else:
        print("   FAIL Data utils returned wrong type")
except Exception as e:
    print(f"   FAIL Data utils error: {e}")

print("\n=== Test Complete ===")
