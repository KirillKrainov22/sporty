import sys
sys.path.insert(0, '.')
try:
    exec(open('app.py').read().split('st.title')[0])
    print("SUCCESS: All imports work")
except Exception as e:
    print(f"ERROR: {type(e).__name__}")
