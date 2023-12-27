import os

DEVELOPER_TOKEN = os.environ.get('GOOGLE_DEVELOPER_TOKEN')
MANAGER_ID = os.environ.get('GOOGLE_LOGIN_CUSTOMER_ID')

class Headers:
    
    def __init__(self, access_token):
        self._access_token = access_token
    
    def custom_headers (self) -> dict:
        return {
            'Authorization': f'Bearer {self._access_token}',
            'developer-token': DEVELOPER_TOKEN,
            'login-customer-id': MANAGER_ID,
            'Host': 'googleads.googleapis.com',
            'Content-Type': 'application/json'
        }
        
