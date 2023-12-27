#!/usr/bin/env python
# Copyright 2020 Google LLC
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
"""Adds a customizer attribute.

Also links the customizer attribute to a customer, and then adds a responsive
search ad with a description using the ad customizer to the specified ad group.

Customizer attributes and ad group customizers are created for business data
customizers. For more information about responsive search ad customization see:
https://developers.google.com/google-ads/api/docs/ads/customize-responsive-search-ads?hl=en
"""


import argparse
from datetime import date, timedelta
import sys
from uuid import uuid4
from faker import Faker

_CUSTOMIZER_ATTRIBUTE_NAME = "Allegiant"

def generate_random_name():
    fake = Faker()
    return fake.name()

def responsive_search_ad(client, customer_id, ad_group_id, ads_details):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        ad_group_id: an ad group ID.
        customizer_attribute_name: the name for the customizer attribute.
    """
    customizer_attribute_name = generate_random_name()
    try:

        customizer_attribute_resource_name = create_customizer_attribute(
            client, customer_id, customizer_attribute_name
        )

        link_customizer_attribute_to_customer(
            client, customer_id, customizer_attribute_resource_name
        )

        create_responsive_search_ad_with_customization(
            client, customer_id, ad_group_id, ads_details
        )
        return True
    except Exception as ex:
        print('Error Occur in Responsive Search Ad', ex)
        return False


def create_customizer_attribute(client, customer_id, customizer_attribute_name):
    """Creates a customizer attribute with the given customizer attribute name.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        customizer_attribute_name: the name for the customizer attribute.

    Returns:
        A resource name for a customizer attribute.
    """
    # Creates a customizer attribute operation for creating a customizer
    # attribute.
    operation = client.get_type("CustomizerAttributeOperation")
    # Creates a customizer attribute with the specified name.
    customizer_attribute = operation.create
    customizer_attribute.name = customizer_attribute_name
    # Specifies the type to be 'PRICE' so that we can dynamically customize the
    # part of the ad's description that is a price of a product/service we
    # advertise.
    customizer_attribute.type_ = client.enums.CustomizerAttributeTypeEnum.PRICE

    # Issues a mutate request to add the customizer attribute and prints its
    # information.
    customizer_attribute_service = client.get_service(
        "CustomizerAttributeService"
    )
    response = customizer_attribute_service.mutate_customizer_attributes(
        customer_id=customer_id, operations=[operation]
    )
    resource_name = response.results[0].resource_name

    print(f"Added a customizer attribute with resource name: '{resource_name}'")

    return resource_name


def link_customizer_attribute_to_customer(
    client, customer_id, customizer_attribute_resource_name, ads_budget=10
):
    """Links the customizer attribute to the customer.

    This is done by providing a value to be used in a responsive search ad
    that will be created in a later step.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        customizer_attribute_resource_name: a resource name for  customizer
            attribute.
    """
    # Creates a customer customizer operation.
    operation = client.get_type("CustomerCustomizerOperation")
    # Creates a customer customizer with the value to be used in the responsive
    # search ad.
    customer_customizer = operation.create
    customer_customizer.customizer_attribute = (
        customizer_attribute_resource_name
    )
    customer_customizer.value.type_ = (
        client.enums.CustomizerAttributeTypeEnum.PRICE
    )
    # Specify '100USD' as a text value. The ad customizer will dynamically
    # replace the placeholder with this value when the ad serves.
    customer_customizer.value.string_value = f"{ads_budget}USD"

    customer_customizer_service = client.get_service(
        "CustomerCustomizerService"
    )
    # Issues a mutate request to add the customer customizer and prints its
    # information.
    response = customer_customizer_service.mutate_customer_customizers(
        customer_id=customer_id, operations=[operation]
    )
    resource_name = response.results[0].resource_name

    print(f"Added a customer customizer with resource name: '{resource_name}'")


def create_responsive_search_ad_with_customization(
    client, customer_id, ad_group_id, ads_details: dict
):
    """Creates a responsive search ad using the specified customizer attribute.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        ad_group_id: an ad group ID.
        customizer_attribute_name: the name for the customizer attribute.
    """
    # Creates an ad group ad operation.
    operation = client.get_type("AdGroupAdOperation")
    # Creates an ad group ad.
    ad_group_ad = operation.create
    ad_group_service = client.get_service("AdGroupService")
    ad_group_ad.ad_group = ad_group_service.ad_group_path(
        customer_id, ad_group_id
    )
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.PAUSED
    #  Creates an ad and sets responsive search ad info.
    ad = ad_group_ad.ad
    
    final_url = ads_details.get('final_url')
    ad.final_urls.append(final_url)

    headline1 = client.get_type('AdTextAsset')
    headline1.text = ads_details.get('headline1')

    headline2 = client.get_type('AdTextAsset')
    headline2.text = ads_details.get('headline2')

    headline3 = client.get_type('AdTextAsset')
    headline3.text = ads_details.get('headline3')

    ad.responsive_search_ad.headlines.extend(
        [headline1, headline2, headline3]
    )

    description1 = client.get_type("AdTextAsset")
    description1.text = ads_details.get('description1')
    
    description2 = client.get_type("AdTextAsset")
    description2.text = ads_details.get('description2')

    ad.responsive_search_ad.descriptions.extend([description1, description2])

    ad.responsive_search_ad.path1 = ads_details.get('path1')
    ad.responsive_search_ad.path2 = ads_details.get('path2')
    # Issues a mutate request to add the ad group ad and prints its information.
    ad_group_ad_service = client.get_service("AdGroupAdService")
    response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id=customer_id, operations=[operation]
    )
    resource_name = response.results[0].resource_name

    print(f"Created responsive search ad with resource name: '{resource_name}'")
