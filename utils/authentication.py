import requests
import os
from requests.auth import AuthBase
# from .access_token import access_token


DEVELOPER_TOKEN = os.environ.get('GOOGLE_DEVELOPER_TOKEN')
MANAGER_ID = os.environ.get('GOOGLE_LOGIN_CUSTOMER_ID')
ACCESS_TOKEN = 'ya29.a0AfB_byAy7mWWVvlI6z4yPAae7qpD27GU7TP_90sBTyWAO7pf5t69os1ybqvqlUO6l-CuKKcW2Cx1-F3RjGWYLwSDbBEuuPjYM5x7ZVmcBi8mmrvO3-kvor8pZ4Zs07rV48IYFy597XvGkYWNRyF5AyVg0vXXX3v0DdiBvAaCgYKAW0SARASFQHGX2MiiM4Wn7uZJ_EsIm_epegvHA0173'

class InternalAuth(AuthBase):
    """
    """

    def __init__(self):
        self.token = ACCESS_TOKEN
    
    def __call__(self, request):

        request.headers['Authorization'] = f'Bearer {self.token}'
        request.headers['developer-token'] =  DEVELOPER_TOKEN
        request.headers['login-customer-id'] = MANAGER_ID

        return request