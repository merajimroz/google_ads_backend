# Generated by Django 3.2.4 on 2022-02-18 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_createsmartcampaign_business_location_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='EditGeoTargets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refreshToken', models.CharField(blank=True, max_length=500)),
                ('customer_id', models.CharField(max_length=500)),
                ('campaign_id', models.CharField(max_length=500)),
                ('new_geo_target_names', models.CharField(max_length=500)),
                ('country_code', models.CharField(max_length=500)),
                ('language_code', models.CharField(max_length=500)),
            ],
        ),
    ]
