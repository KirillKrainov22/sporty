print("Тестируем импорты...")
try:
    from modules.api_client import api
    print("✅ api_client импортирован")
    
    from modules.cache import cache
    print("✅ cache импортирован")
    
    from modules.mock_data import MOCK_DATA
    print("✅ mock_data импортирован")
    
    from modules.data_utils import prepare_chart_data
    print("✅ data_utils импортирован")
    
    print("\n🎉 Все импорты работают!")
except Exception as e:
    print(f"\n❌ Ошибка: {type(e).__name__}: {e}")
