import sys
sys.path.insert(0, '.')

print("Testing full app.py imports...")
try:
    exec(open('app.py').read().split('st.title')[0])
    print("SUCCESS: All imports work")
    
    # Check we have all needed objects
    for obj in ['api', 'cache', 'MOCK_DATA']:
        if obj in locals():
            print(f"  ✓ {obj} available")
        else:
            print(f"  ✗ {obj} missing")
            
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
