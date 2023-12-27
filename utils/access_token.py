import requests
import time

class AccessToken:

    def __init__(self, refresh_token):
        self._refresh_token = refresh_token
        self._access_token = None
        self._token_expiry = 0

    def get_access_token(self) -> str:
        try: 
            if time.time() >= self._token_expiry or (self._access_token is None):
                url = 'https://www.googleapis.com/oauth2/v3/token'
                payload = {
                    'grant_type': 'refresh_token',
                    'client_id': '879681125054-mcm1erb8au7v064id9fv5q0ehtnq0c98.apps.googleusercontent.com',
                    'client_secret': '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',
                    'refresh_token': self._refresh_token
                }

                response = requests.post(url, data=payload)
                if response.status_code == 200:
                    print('Token Refreshed successfully.')
                    token_data = response.json()
                    access_token = token_data['access_token']
                    self._token_expiry = time.time() + token_data['expires_in']  # Set the token expiry time
                    print(access_token)
                else:
                    print('Token Refresh Failed with status code:', response.status_code)
                    print(response.text)

        except Exception as ex:
            print('Exception Occur in Fetching Access Token', ex)
            pass
        
        return access_token
    
class Token:

    def __init__(self, refresh_token):
        self._access_token = None
        self._refresh_token = refresh_token
    
    @property
    def access_token(self):
        if self._access_token is None:
            self._access_token = AccessToken(self._refresh_token)
        return self._access_token
    