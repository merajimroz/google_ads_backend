
from rest_framework import serializers

# adflare imports
from adflare.models import CreateCampaignModel, AdGroupModel, UserModel, GoogleAuthModel

class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            'email',
            'password'
        ]

class CreateSmartCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateCampaignModel
        fields = [
            'mytoken',
            'budget',
            'campaign_name',
            'customer_id'
        ] 

class AdGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdGroupModel
        fields = [
            'adgroup_name',
            'campaign_id',
            'customer_id',
            'bid_amount'
        ]

class GoogleAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleAuthModel
        fields = [
            'google_access_code',
            'refresh_token',
            'token'
        ]