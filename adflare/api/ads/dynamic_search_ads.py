
#!/usr/bin/env python
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This code example adds a new dynamic search ad (DSA).

It also creates a webpage targeting criteria for the DSA.
"""


import argparse
from datetime import datetime, timedelta
import sys
from uuid import uuid4

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def dynamic_search_ad(client, customer_id, adgroup_name, criterion_name, ad_description ):
    
    try:
        create_expanded_dsa(client, customer_id, adgroup_name, ad_description)
        # add_webpage_criterion(client, customer_id, adgroup_name, criterion_name, 50000000)
        return True
    
    except GoogleAdsException as ex:
        return False


def create_expanded_dsa(client, customer_id, ad_group_resource_name, ad_description):
    """Creates a dynamic search ad under the given ad group.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        ad_group_resource_name: a resource_name str for an Ad Group.
    """
    # Retrieve a new ad group ad operation object.
    ad_group_ad_operation = client.get_type("AdGroupAdOperation")
    # Create and expanded dynamic search ad. This ad will have its headline,
    # display URL and final URL auto-generated at serving time according to
    # domain name specific information provided by DynamicSearchAdSetting at
    # the campaign level.
    ad_group_ad = ad_group_ad_operation.create
    # Optional: set the ad status.
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.PAUSED
    # Set the ad description.
    ad_group_ad.ad.expanded_dynamic_search_ad.description = ad_description
    ad_group_ad.ad_group = ad_group_resource_name

    # Retrieve the ad group ad service.
    ad_group_ad_service = client.get_service("AdGroupAdService")

    # Submit the ad group ad operation to add the ad group ad.
    response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id=customer_id, operations=[ad_group_ad_operation]
    )
    resource_name = response.results[0].resource_name
    print(f'Created Ad Group Ad with resource_name: "{resource_name}"')
    return resource_name


def add_webpage_criterion(client, customer_id, ad_group_resource_name, criterion_name, bid_value=10000000):
    """Creates a web page criterion to the given ad group.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        ad_group_resource_name: a resource_name str for an Ad Group.
    """
    # Retrieve a new ad group criterion operation.
    ad_group_criterion_operation = client.get_type("AdGroupCriterionOperation")
    # Create an ad group criterion for special offers for Mars Cruise.
    criterion = ad_group_criterion_operation.create
    criterion.ad_group = ad_group_resource_name
    # Optional: set custom bid amount.
    criterion.cpc_bid_micros = bid_value
    # Optional: set the status.
    criterion.status = client.enums.AdGroupCriterionStatusEnum.PAUSED

    # Sets the criterion to match a specific page URL and title.
    criterion.webpage.criterion_name = criterion_name
    # First condition info - URL
    webpage_condition_info_url = client.get_type("WebpageConditionInfo")
    webpage_condition_info_url.operand = (
        client.enums.WebpageConditionOperandEnum.URL
    )
    webpage_condition_info_url.argument = "https://adflare.allegiantglobal.io"
    # Second condition info - Page title
    webpage_condition_info_page_title = client.get_type("WebpageConditionInfo")
    webpage_condition_info_page_title.operand = (
        client.enums.WebpageConditionOperandEnum.PAGE_TITLE
    )
    webpage_condition_info_page_title.argument = "Special Offer"
    # Add first and second condition info
    criterion.webpage.conditions.extend(
        [webpage_condition_info_url, webpage_condition_info_page_title]
    )

    # Retrieve the ad group criterion service.
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    # Issues a mutate request to add the ad group criterion.
    response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id, operations=[ad_group_criterion_operation]
    )
    resource_name = response.results[0].resource_name

    print(f'Created Ad Group Criterion with resource_name: "{resource_name}"')
    