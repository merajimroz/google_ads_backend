import os
import uuid
from datetime import datetime, timedelta
import pandas as pd
import io
from django.http import HttpResponse
import xlsxwriter

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers, status
from django.views.decorators.csrf import csrf_exempt
from google.ads.googleads.client import GoogleAdsClient
from django.contrib.auth.models import User
from django.http import FileResponse, HttpResponse
from pathlib import Path

# github imports
from api.get_user_credentials import get_refresh_token
from api.authenticate import connect, get_token

# adflare imports
from adflare.api.campaign.create_campaign import create_campaign
from adflare.api.campaign.get_campaign import get_campaigns
from adflare.api.adgroups.add_ad_groups import add_adgroups, ad_group_for_responsive_search_ads
from adflare.api.adgroups.get_ad_groups import get_adgroups
from adflare.api.ads.dynamic_search_ads import dynamic_search_ad
from adflare.api.ads.responsive_search_ads import responsive_search_ad
from adflare.api.ads.get_search_ads import get_google_dynamic_search_ads
from adflare.api.account_management.get_account_hierachy import get_account_list
from adflare.serializers import CreateSmartCampaignSerializer, AdGroupSerializer, LoginUserSerializer, GoogleAuthSerializer
from adflare.models import UserModel, GoogleAuthModel
from utils.access_token import Token
from adflare.api.google_ads_with_excel import google_ads_with_excel 

CLIENT_ID = '2215958043'
CAMPAIGN_ID = '20856085585'
MANAGER_ID = os.environ.get('GOOGLE_LOGIN_CUSTOMER_ID')
REFRESH_TOKEN = '1//0gUY_vUaclG6uCgYIARAAGBASNwF-L9IrqeT2Gv8WHB92LKtd2YyFjd6RvDXG5vX4heb4jxD9qm3azC5fsPdIZvxsgUY3vNGpemQ'


lifetime_of_access_token = datetime.now() + timedelta(minutes=60)
access_token = 'ya29.a0AfB_byDRtSMoEoQOyliEUz2S4c9kT8Jdm_7ViFswW1KGdvCxGw1yP8-Z_mXKxGZ80PPFgs-ZzOsbbmTQQNaRKP_M8dX0YjabByaAipW3-Yn_SUdWv9a-DWBQEGbUx_UpG10HMXiXmYfzkGzlyxDYfmA2Gitz_8eNiTpoyAaCgYKAQQSARASFQHGX2MiE-N1CutNi_sW5VHzK-_PFw0173'

def google_access_token(refresh_token):

    global lifetime_of_access_token, access_token

    if (datetime.now() > lifetime_of_access_token) or (access_token is None):
        token = Token(refresh_token).access_token
        access_token = token.get_access_token()
        lifetime_of_access_token = datetime.now() + timedelta(minutes=359)

    return access_token

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def configure_credentials(refresh_token):

    # Configurations
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
    GOOGLE_DEVELOPER_TOKEN = os.environ.get("GOOGLE_DEVELOPER_TOKEN", None)
    GOOGLE_LOGIN_CUSTOMER_ID = os.environ.get("GOOGLE_LOGIN_CUSTOMER_ID", None)

    credentials = {
    "developer_token": GOOGLE_DEVELOPER_TOKEN,
    "refresh_token": refresh_token,
    "client_id": GOOGLE_CLIENT_ID,
    "client_secret": GOOGLE_CLIENT_SECRET,
    "login_customer_id": GOOGLE_LOGIN_CUSTOMER_ID,
    "use_proto_plus": True}

    client = GoogleAdsClient.load_from_dict(credentials)
    return client

@api_view(['POST', 'GET'])
def create_campaign_view(request):
    if request.method == 'POST':
        """
        Requirements - 
        1. Token,
        2. Campaign Name,
        3. Customer Id,
        4. Budget Amount

        """
        data = {
            'mytoken': request.data.get('mytoken'),
            'campaign_name': request.data.get('campaignName'),
            'customer_id': request.data.get('customer_id'),
            'budget': request.data.get('budget')
        }
        serializer = CreateSmartCampaignSerializer(data=data)
        if serializer.is_valid():
            print('CreateSmartCampaignSerializer is valid')

            # get the token associated with that user
            mytoken = serializer['mytoken'].value
            refresh_token = get_refresh_token(mytoken)

            campaign_name = serializer.data.get('campaign_name')
            if campaign_name is None:
                campaign_name = f'Campaign - {uuid.uuid4()}'

            budget_amt = serializer.data.get('budget')    
            client = configure_credentials(refresh_token)
            create_campaign(client, CLIENT_ID, campaign_name, budget_amt)

            return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_adgroups_view(request):
    if request.method == 'POST':
        '''
        Requirements - 
        2. Customer id,
        3. Campaign id,
        4. Adgroup Name
        5. Bid Amount
        '''

        data = {
            'customer_id': request.data.get('customerId'),
            'campaign_id': request.data.get('campaignId'),
            'adgroup_name': request.data.get('adGroupName'),
            'bid_amount' : request.data.get('bidAmount')
        }

        serializer = AdGroupSerializer(data=data)
        if serializer.is_valid():
            print('Adgroup Serializer is valid')

            # # get the token associated with that user
            # mytoken = serializer['mytoken'].value
            # refresh_token = get_refresh_token(mytoken)
            serializer.save()
            client = configure_credentials(REFRESH_TOKEN)
            campaign_id = serializer.data.get('campaign_id')
            adgroup_name = serializer.data.get('adgroup_name')
            bid_amount = serializer.data.get('bid_amount')
        
            if  adgroup_name is None:
                adgroup_name =  f'AdGroup - {uuid.uuid4()}'

            resource_name = add_adgroups(client, CLIENT_ID, campaign_id, adgroup_name, int(bid_amount))
            return Response(data = resource_name, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def dynamic_search_ad_view(request):
    if request.method == 'POST':
        '''
        Requirements - 
        2. Ad Group Resource Name
        3. Budget Amount
        '''

        # mytoken = request.data.get('mytoken')
        # refresh_token = get_refresh_token(mytoken)
        print(request.data)
        description = request.data.get('adDescription')
        ad_group_resource_name = request.data.get('adGroupResourceName')
        
        client = configure_credentials(REFRESH_TOKEN)   
        
        response = dynamic_search_ad(client, CLIENT_ID, ad_group_resource_name, 'Food & Restaruant', description)

        if response:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

#API endpoint 'api/create-account
@api_view(['POST', 'GET'])
def create_account_view(request):
    '''
    Requirements
    1. Email
    2. Password
    '''

    email = request.data.get('email')
    password = request.data.get('password')

    serializer = LoginUserSerializer(data=request.data)
    if serializer.is_valid():
        User.objects.create_user(username=email, password=password)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

# API Endpoint '/api/login'
@api_view(['POST', 'GET'])
def login_user_view(request):
    '''
    Requirements - 
        1. Email
        2. Password
    '''
    
    if request.method == 'POST':
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            print("Login User Serializer is Valid!")

            email = serializer.data.get('email')
            user = User.objects.get(username = email)

        if user:
            access_token = get_tokens_for_user(user)
            return Response({
                'token': access_token.get('access')
            }, status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)

# Get the authorization URL so user can give consent.
# API endpoint 'api/connect/'
@api_view(['GET'])
def authenticate_view(request):
    if request.method == 'GET':

        # get the url to redirect the user so they can authenticate and authorize your app
        authorization_url = connect()[0]
        passthrough_val = connect()[1]

        data = {
            'url': authorization_url,
            'passthrough_val': passthrough_val
        }

        # return the authorization_url that will be used on the FE to redirect user
        # and user will authenticate themselves and authorize your app permissions
        return Response(data=data, status=status.HTTP_200_OK)

# Callback to get the refresh token and save it to our backend.
# API endpoint 'api/get-token/'
@api_view(['POST'])
def get_token_view(request):
   
    google_access_code = request.data.get('googleAccessCode')
    token = request.data.get('token')
    
    # call the function get_token from the authenticate.py file
    refresh_token = get_token(google_access_code)

    serializer_credentials = GoogleAuthSerializer(data={
        'token': token, 
        'refresh_token': refresh_token,
        'google_access_code': google_access_code
        })

    if serializer_credentials.is_valid():
        print('serializer valid so saving refresh token to RefreshToken model')
        serializer_credentials.save()


        # send to the frontend that user has a refresh token
        return Response({
            'refreshToken' : refresh_token
        }, safe=False)

    return Response(serializer_credentials.errors, status=status.HTTP_400_BAD_REQUEST)

# to get account list
# API endpoint /api/account-list
@api_view(['GET'])
def account_list_view(request):

    '''
    Requirements
    1. Manager ID
    2. Refresh Token
    '''

    # refresh_token = request.data.get('refreshToken')

    client = configure_credentials(REFRESH_TOKEN)
    accounts_list = get_account_list(client, MANAGER_ID)

    return Response(data=accounts_list, status=status.HTTP_200_OK)

# get all campaigns 
# API endpoints /api/campaign/customerid
@api_view(['GET', 'POST'])
def get_campaign_for_customer_view(request, customer_id):
    
    print(customer_id)
    access_token = google_access_token(REFRESH_TOKEN)
    print(access_token)
    campaigns = get_campaigns(customer_id, access_token)

    if campaigns:
        return Response(data=campaigns, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

# get all adgroups
# API endpoints /api/adgroups/customer_id
@api_view(['GET', 'POST'])
def get_adgroups_for_customer_view(request, customer_id, campaign_id):
    
    print(customer_id)
    token = google_access_token(RefreshToken)

    adgroups = get_adgroups(customer_id, token, campaign_id)

    if adgroups:
        return Response(data=adgroups, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

# get all adgroups
# API endpoints /api/customer/customer_id/adgroup/ad_group_id

@api_view(['GET'])
def get_search_ads_view(request, customer_id, ad_group_id):

    try:
        ad_details = get_google_dynamic_search_ads(ad_group_id, customer_id)
        return Response(data=ad_details, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# api endpoint /api/dynamic-search-adgroup/customer_id    
@api_view(['POST'])
def ad_group_for_responsive_search_ads_view(request, customer_id):

    try:

        client = configure_credentials(REFRESH_TOKEN)
        customer_id = CLIENT_ID
        group_name = f'ResponsiveAdGroup - {uuid.uuid4()}'
        bid_amount = 20
        resource_name = ad_group_for_responsive_search_ads(client, customer_id, group_name, bid_amount)

        if resource_name:
            return Response(data=resource_name, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as ex:
        return Response(data = str(ex), status=status.HTTP_400_BAD_REQUEST)

# API endpoint /api/responsive-search-ad
@api_view(['POST'])
def responsive_search_ad_view(request):

    try:
        client = configure_credentials(REFRESH_TOKEN)
        customer_id = request.data.get('customerID')
        ad_group_id = request.data.get('adGroupID')
        ads_details = request.data.get('adDetails')

        headlines = ads_details.get('headlines')
        descriptions = ads_details.get('descriptions')
        paths = ads_details.get('paths')

        details = {
            'headline1': headlines[0],
            'headline2': headlines[1],
            'headline3': headlines[2],
            'description1': descriptions[0],
            'description2': descriptions[1],
            'path1': paths[0],
            'path2': paths[1],
            'final_url': request.data.get('finalURL') 
        }
        result = responsive_search_ad(client, customer_id, ad_group_id, details)
        if result:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

    except Exception as ex:
        return Response(data=str(ex), status=status.HTTP_400_BAD_REQUEST)

# API endpoints /adflare/api/excel-manage-ads
@api_view(['POST', 'GET'])
def excel_sheet_to_create_google_ads_view(request):
    '''
    This view is used to extract data from excel sheet and process and create google ads from it
    '''

    try:
        file = request.data.get('file')
        processed_data = google_ads_with_excel(file)

        client = configure_credentials(REFRESH_TOKEN)
        if processed_data:
            for each_ad_data in processed_data:
                customer_id = str(each_ad_data.get('customer_id'))
                ad_group_id = str(each_ad_data.get('adgroup_id'))
                responsive_search_ad(client, customer_id, ad_group_id, each_ad_data)

        return Response(status=status.HTTP_200_OK)
    except Exception as ex:
        return Response(data=str(ex), status=status.HTTP_400_BAD_REQUEST)


# API endpoints /api/excel-ads-template
@api_view(['GET', 'POST'])
def template_for_excel_ads_with_io_view(request):
    output = io.BytesIO()

     
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    customer_id = request.data.get('customerId')
    ad_group_id = request.data.get('adGroupId')
    campaign_id = request.data.get('campaignId')

    data = [['customer_id', 'ad_group_id', 'campaign_id', 'final_url', 
               'headline1', 'headline2', 'headline3', 
               'description1', 'description2', 'path1',
               'path2', 'type_of_ad'], [customer_id, ad_group_id, campaign_id, '', 
               '', '', '', 
               '', '', '',
               '', '']]
    
    for row_num, col in enumerate(data):
        for col_num, cell_data in enumerate(col):
            worksheet.write(row_num, col_num, cell_data)

    # Close the workbook before sending the data.
    workbook.close()

    # Rewind the buffer.
    output.seek(0)

    # Set up the Http response.
    filename = "ads_template.xlsx"
    response = HttpResponse(
        output,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f"attachment; filename={filename}"

    return response