import requests
import os
from utils.headers import Headers

def get_adgroups(customer_id, access_token, campaign_id):
    records = []

    query = """
        SELECT ad_group.id, ad_group.name, ad_group.status, 
        ad_group.resource_name, ad_group.type 
        FROM ad_group"""

    # Issues a search request using streaming.
    
    url = f'{os.environ.get("GOOGLE_REST_INTERFACE_API_URL")}/customers/{customer_id}/googleAds:search'

    headers = Headers(access_token).custom_headers()
    response = requests.post(url, headers=headers, json={'query': query})

    if(response.ok):

        results = response.json().get('results')
        print(results)
        for row in results:
            adgroup = row.get('adGroup')
            print(
                f"Adgroup with ID {adgroup.get('id')} and name "
                f"{adgroup.get('name')} was found."
            )
            status = adgroup.get('status')
            if status in ['PAUSED', 'ENABLED']:
                records.append({
                    'id': adgroup.get('id'),
                    'name': adgroup.get('name'),
                    "status": adgroup.get('status'),
                    'type': adgroup.get('type')
                })
        return records
    
    else:
        return None