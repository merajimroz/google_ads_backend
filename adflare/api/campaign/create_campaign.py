import datetime
from google.ads.googleads.errors import GoogleAdsException

_DATE_FORMAT = "%Y%m%d"

def create_campaign(client, customer_id, campaign_name, campaign_budget_amount):

    campaign_budget_service = client.get_service("CampaignBudgetService")
    campaign_service = client.get_service("CampaignService")

    # Create a campaign budget
    campaign_budget_operation = client.get_type("CampaignBudgetOperation")
    campaign_budget = campaign_budget_operation.create
    campaign_budget.name = f'Budget-{campaign_name}'
    print('campagin budget name', campaign_budget.name)
    campaign_budget.delivery_method = (
        client.enums.BudgetDeliveryMethodEnum.STANDARD
    )
    campaign_budget.amount_micros = campaign_budget_amount*1000
    
    campaign_budget_response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=customer_id, operations=[campaign_budget_operation]
    )

    # Create a campaign
    campaign_operation = client.get_type("CampaignOperation")
    campaign = campaign_operation.create
    campaign.name = campaign_name
    campaign.advertising_channel_type = (
        client.enums.AdvertisingChannelTypeEnum.SEARCH
    )
    campaign.status = client.enums.CampaignStatusEnum.PAUSED
    campaign.dynamic_search_ads_setting.domain_name = "adflare.allegiantglobal.io"
    campaign.dynamic_search_ads_setting.language_code = "en"

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
            customer_id=customer_id, operations=[campaign_operation]
        )
        print('campaign response', campaign_response)
        resource_name = campaign_response.results[0].resource_name
        campaign_id = resource_name.split('/')[3]
        return campaign_id
    except GoogleAdsException as ex:
        # Handle exception
        pass