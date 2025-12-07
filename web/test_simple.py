try:
    from modules.api_client import api
    print("SUCCESS: api imported")
    
    # Проверим что clear_cache внутри класса
    if hasattr(api, 'clear_cache'):
        print("SUCCESS: clear_cache is a method of api")
    else:
        print("ERROR: clear_cache not found in api")
        
except Exception as e:
    print(f"ERROR: {type(e).__name__}")
