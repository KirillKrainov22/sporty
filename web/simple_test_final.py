import sys
sys.path.insert(0, '.')
print("Simple import test...")

modules_to_test = [
    ('streamlit', 'st'),
    ('plotly.graph_objects', 'go'),
    ('plotly.express', 'px'),
    ('pandas', 'pd'),
    ('modules.api_client', 'api'),
    ('modules.cache', 'cache'),
    ('modules.mock_data', 'MOCK_DATA'),
    ('modules.data_utils', 'prepare_chart_data')
]

all_ok = True
for module, name in modules_to_test:
    try:
        if '.' in module:
            # Для модулей с точкой используем __import__
            __import__(module)
            print(f"  ✓ {module}")
        else:
            exec(f"import {module}")
            print(f"  ✓ {module}")
    except Exception as e:
        print(f"  ✗ {module}: {type(e).__name__}")
        all_ok = False

if all_ok:
    print("\n✅ ALL IMPORTS WORK!")
else:
    print("\n❌ SOME IMPORTS FAILED")
