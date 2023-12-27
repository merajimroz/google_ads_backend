
_CAMPAIGN_RESOURCE_NAME  = 'customers/2215958043/campaigns/20856085585'

def add_adgroups(client, customer_id, campaign_id, group_name, bid_amount) -> str:
    ad_group_service = client.get_service("AdGroupService")
    campaign_service = client.get_service("CampaignService")

    # Create ad group.
    ad_group_operation = client.get_type("AdGroupOperation")
    ad_group = ad_group_operation.create
    ad_group.name = group_name
    ad_group.status = client.enums.AdGroupStatusEnum.PAUSED
    ad_group.campaign = campaign_service.campaign_path(customer_id, campaign_id)
    # ad_group.campaign = _CAMPAIGN_RESOURCE_NAME
    ad_group.type_ = client.enums.AdGroupTypeEnum.SEARCH_DYNAMIC_ADS
    ad_group.cpc_bid_micros = bid_amount*1000000
    ad_group.tracking_url_template = (
        "http://tracker.example.com/traveltracker/{escapedlpurl}"
    )
    # Add the ad group.
    ad_group_response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id, operations=[ad_group_operation]
    )
    print('Adgroup Response', ad_group_response)
    resource_name = ad_group_response.results[0].resource_name

    return resource_name


def ad_group_for_responsive_search_ads(client, customer_id, group_name, bid_amount):
    ad_group_service = client.get_service("AdGroupService")
    campaign_service = client.get_service("CampaignService")

    # Create ad group.
    ad_group_operation = client.get_type("AdGroupOperation")
    ad_group = ad_group_operation.create
    ad_group.name = group_name
    ad_group.status = client.enums.AdGroupStatusEnum.PAUSED
    # ad_group.campaign = campaign_service.campaign_path(customer_id, campaign_id)
    ad_group.campaign = _CAMPAIGN_RESOURCE_NAME
    ad_group.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
    ad_group.cpc_bid_micros = bid_amount*1000000
    ad_group.tracking_url_template = (
        "http://tracker.example.com/traveltracker/{escapedlpurl}"
    )
    # Add the ad group.
    ad_group_response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id, operations=[ad_group_operation]
    )
    print('Adgroup Response', ad_group_response)
    resource_name = ad_group_response.results[0].resource_name

    return resource_name