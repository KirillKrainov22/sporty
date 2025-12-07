import sys
sys.path.insert(0, '.')
print("Testing imports...")
try:
    exec(open('app.py').read().split('st.title')[0])
    print("SUCCESS: All imports work")
    
    # Check we have the objects
    for obj in ['api', 'cache', 'MOCK_DATA']:
        if obj in locals():
            print(f"  OK: {obj}")
        else:
            print(f"  MISSING: {obj}")
            
except Exception as e:
    print(f"ERROR: {type(e).__name__}")
    print(f"Details: {e}")
