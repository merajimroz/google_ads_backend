import requests
import os
from utils.headers import Headers

def get_campaigns(customer_id, access_token):
    records = []

    query = """
        SELECT campaign.id, campaign.name, campaign.status,  campaign.advertising_channel_type FROM campaign"""

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
            status = campaign.get('status')

            if status in ['ENABLED', 'PAUSED']:
                records.append({
                    'campaignId': campaign.get('id'),
                    'campaignName': campaign.get('name'),
                    'status': campaign.get('status'),
                    'advertisingChannelType': campaign.get('advertisingChannelType')
                })
        return records
    
    else:
        print(response.json())
        return None