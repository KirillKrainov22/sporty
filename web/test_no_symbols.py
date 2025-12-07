import sys
sys.path.insert(0, '.')
print("Testing imports (no symbols)...")

# Test core imports
core_modules = ['streamlit', 'plotly.graph_objects', 'plotly.express', 'pandas']
for module in core_modules:
    try:
        __import__(module)
        print(f"PASS: {module}")
    except ImportError as e:
        print(f"FAIL: {module} - {e}")

print("\\nTesting our modules...")
# Test our modules
our_modules = [
    ('modules.api_client', 'api'),
    ('modules.cache', 'cache'),
    ('modules.mock_data', 'MOCK_DATA'),
    ('modules.data_utils', 'prepare_chart_data')
]

for module, obj in our_modules:
    try:
        imported = __import__(module, fromlist=[obj])
        if hasattr(imported, obj):
            print(f"PASS: {module}.{obj}")
        else:
            print(f"FAIL: {module} has no {obj}")
    except Exception as e:
        print(f"FAIL: {module} - {type(e).__name__}")

print("\\nTest complete.")
