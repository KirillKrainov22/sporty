import sys
sys.path.insert(0, '.')
try:
    from modules.api_client import api
    print('SUCCESS: api_client imported')
    print('API URL:', api.base_url)
except Exception as e:
    print('ERROR:', type(e).__name__, ':', str(e)[:100])
