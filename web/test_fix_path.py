import sys
import os

# Добавляем текущую директорию в путь
sys.path.insert(0, os.getcwd())
print("Current dir:", os.getcwd())
print("Python path first 3:", sys.path[:3])

try:
    from modules.api_client import api
    print("\n✅ SUCCESS: Import worked!")
    
    # Проверим методы
    methods = ['get_user_stats', 'clear_cache']
    for method in methods:
        if hasattr(api, method):
            print(f"✅ {method} exists")
        else:
            print(f"❌ {method} missing")
            
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
