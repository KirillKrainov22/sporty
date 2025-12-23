import os

USE_API = os.environ.get('USE_API', 'true').lower() == 'true'
API_BASE_URL = os.environ.get('API_BASE_URL', 'http://api:8000')
CACHE_TTL = int(os.environ.get('CACHE_TTL', '60'))
TEST_USER_ID = int(os.environ.get('TEST_USER_ID', '1'))
ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN', '')
