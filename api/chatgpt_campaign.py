import datetime
import uuid
import os
import argparse

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

_DATE_FORMAT = "%Y%m%d"

def create_campaign(customer_id, use_login_id, refresh_token):

    # Configurations
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
    GOOGLE_DEVELOPER_TOKEN = os.environ.get("GOOGLE_DEVELOPER_TOKEN", None)
    GOOGLE_LOGIN_CUSTOMER_ID = os.environ.get("GOOGLE_LOGIN_CUSTOMER_ID", None)
    
     # Configure using dictionary.
    # Check if we need to use login_customer_id in the headers,
    # which is needed if the Ads account was created by the app.
    if use_login_id == True:
        credentials = {
        "developer_token": GOOGLE_DEVELOPER_TOKEN,
        "refresh_token": refresh_token,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "login_customer_id": GOOGLE_LOGIN_CUSTOMER_ID,
        "use_proto_plus": True}
    else:
        credentials = {
        "developer_token": GOOGLE_DEVELOPER_TOKEN,
        "refresh_token": refresh_token,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        # "login_customer_id": GOOGLE_LOGIN_CUSTOMER_ID,
        "linked_customer_id": customer_id,
        "use_proto_plus": True}

    client = GoogleAdsClient.load_from_dict(credentials)
    print("client initiated...")

    campaign_budget_service = client.get_service("CampaignBudgetService")
    campaign_service = client.get_service("CampaignService")

    # Create a campaign budget
    campaign_budget_operation = client.get_type("CampaignBudgetOperation")
    campaign_budget = campaign_budget_operation.create
    campaign_budget.name = f"My Campaign Budget {uuid.uuid4()}"
    print('campagin budget name', campaign_budget.name)
    campaign_budget.delivery_method = (
        client.enums.BudgetDeliveryMethodEnum.STANDARD
    )
    campaign_budget.amount_micros = 50000
    
    
    print("campaign budget response")
    campaign_budget_response = campaign_budget_service.mutate_campaign_budgets(
        customer_id='2609465919', operations=[campaign_budget_operation]
    )

    print("campaign Budget response", campaign_budget_response)


    # Create a campaign
    campaign_operation = client.get_type("CampaignOperation")
    campaign = campaign_operation.create
    campaign.name = f"My Campaign {uuid.uuid4()}"
    campaign.advertising_channel_type = (
        client.enums.AdvertisingChannelTypeEnum.SEARCH
    )
    campaign.status = client.enums.CampaignStatusEnum.PAUSED

    # Set the bidding strategy and link to the created campaign budget
    campaign.manual_cpc.enhanced_cpc_enabled = True
    campaign.campaign_budget = campaign_budget_response.results[0].resource_name

    # Set network settings
    campaign.network_settings.target_google_search = True
    campaign.network_settings.target_search_network = True
    campaign.network_settings.target_partner_search_network = False
    campaign.network_settings.target_content_network = True

    # Set start and end dates
    start_time = datetime.date.today() + datetime.timedelta(days=1)
    campaign.start_date = datetime.date.strftime(start_time, _DATE_FORMAT)
    end_time = start_time + datetime.timedelta(weeks=4)
    campaign.end_date = datetime.date.strftime(end_time, _DATE_FORMAT)

    try:
        campaign_response = campaign_service.mutate_campaigns(
            customer_id='2609465919', operations=[campaign_operation]
        )
        print(f"Created campaign {campaign_response.results[0].resource_name}.")
    except GoogleAdsException as ex:
        # Handle exception
        pass
        
    
    get_campaigns(client, '2609465919')

    
def get_campaigns(client, customer_id):
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
          campaign.id,
          campaign.name
        FROM campaign
        ORDER BY campaign.id"""

    # Issues a search request using streaming.
    stream = ga_service.search_stream(customer_id=customer_id, query=query)

    print(stream)
    for batch in stream:
        for row in batch.results:
            print(
                f"Campaign with ID {row.campaign.id} and name "
                f'"{row.campaign.name}" was found.'
            )

def create_customer(client, manager_customer_id):
    customer_service = client.get_service("CustomerService")
    customer = client.get_type("Customer")
    now = datetime.date.today().strftime("%Y%m%d %H:%M:%S")
    customer.descriptive_name = f"Account created with CustomerService on {now}"
    # For a list of valid currency codes and time zones see this documentation:
    # https://developers.google.com/google-ads/api/reference/data/codes-formats
    customer.currency_code = "USD"
    customer.time_zone = "America/New_York"
    # The below values are optional. For more information about URL
    # options see: https://support.google.com/google-ads/answer/6305348
    customer.tracking_url_template = "{lpurl}?device={device}"
    customer.final_url_suffix = (
        "keyword={keyword}&matchtype={matchtype}" "&adgroupid={adgroupid}"
    )

    response = customer_service.create_customer_client(
        customer_id=manager_customer_id, customer_client=customer
    )
    print(
        f'Customer created with resource name "{response.resource_name}" '
        f'under manager account with ID "{manager_customer_id}".'
    )