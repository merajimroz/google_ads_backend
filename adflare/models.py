from django.db import models

# User Model
class UserModel(models.Model):
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=25)

# campaign model
class CreateCampaignModel(models.Model):
    mytoken = models.CharField(max_length=500)
    budget = models.PositiveIntegerField()
    campaign_name = models.CharField(max_length=500)
    customer_id = models.CharField(max_length=500)

# Adgroup Model
class AdGroupModel(models.Model):
    adgroup_name = models.CharField(max_length=500)
    campaign_id = models.CharField(max_length=30)
    customer_id = models.CharField(max_length=500)
    bid_amount = models.CharField(max_length=500)

class GoogleAuthModel(models.Model):
    token = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500)
    google_access_code = models.CharField(max_length=500)