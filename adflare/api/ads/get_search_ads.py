import requests
import os
import json

# from utils.authentication import InternalAuth

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
    
def get_google_dynamic_search_ads(ad_group_id, customer_id=2215958043):

    base_url = os.environ.get('GOOGLE_REST_INTERFACE_API_URL')
    url = f'{base_url}/customers/{customer_id}/googleAds:search'
    
    '''
    Query to get dynamic search ads fields.
    '''
 
    query = f'SELECT ad_group_ad.ad.display_url, ad_group_ad.ad.expanded_dynamic_search_ad.description, ad_group_ad.ad.expanded_dynamic_search_ad.description2, ad_group_ad.ad.name, ad_group_ad.ad.resource_name FROM ad_group_ad WHERE customer.id = {customer_id} AND ad_group.id = {ad_group_id}'
             

    response = requests.post(url, auth=InternalAuth(), data=query, verify=False)
    print(response.json())
    results = response.json()['results']

    if(response.ok):
        details = []
        for records in results:
            ad_group_ad = records.get('adGroupAd')
            ad_description = ad_group_ad.get('ad')['expandedDynamicSearchAd']
            ad_id = ad_group_ad.get('resourceName').split('~')[-1]
            resource_name = ad_group_ad.get('resourceName').split('~')[0]
            customer_id = resource_name.split('/')[1]
            ad_group_id = resource_name.split('/')[3]
            
            details.append({
                'ad_group_ad_resource_name': ad_group_ad.get('resourceName'),
                'ad_description': ad_description.get('description'),
                'customer_id': customer_id,
                'ad_group_id': ad_group_id,
                'dynamic_search_ad_id': ad_id
            })

        return (json.dumps(details, indent=2))

if __name__ == '__main__':
    res = get_google_dynamic_search_ads(151677558690, 2215958043)
    print(res)