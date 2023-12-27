import requests
import os
from utils.headers import Headers

def get_campaigns(customer_id, access_token):
    records = []

    query = """
        SELECT
          campaign.id,
          campaign.name
        FROM campaign
        ORDER BY campaign.id"""

    url = f'{os.environ.get("GOOGLE_REST_INTERFACE_API_URL")}/customers/{customer_id}/googleAds:search'

    headers = Headers(access_token).custom_headers()
    response = requests.post(url, headers=headers, json={'query': query})

    if(response.ok):

        results = response.json().get('results')
        for row in results:
            campaign = row.get('campaign')
            print(
                f"Campaign with ID {campaign.get('id')} and name "
                f"{campaign.get('name')} was found."
            )
            records.append({
                'campaignId': campaign.get('id'),
                'campaignName': campaign.get('name')
            })

        return records
    
    else:
        print(response.json())
        return None