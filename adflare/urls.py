from django.urls import path
from adflare.views import ( create_campaign_view, 
                        dynamic_search_ad_view, authenticate_view, get_token_view,
                        create_account_view, login_user_view, account_list_view,
                        get_campaign_for_customer_view, get_adgroups_for_customer_view,
                        get_search_ads_view, add_adgroups_view, ad_group_for_responsive_search_ads_view,
                        responsive_search_ad_view, excel_sheet_to_create_google_ads_view,
                        template_for_excel_ads_with_io_view)

urlpatterns = [
    path('api/create-campaign', create_campaign_view),
    path('api/dynamic-search-ads', dynamic_search_ad_view),
    path('api/connect', authenticate_view),
    path('api/get-token', get_token_view),
    path('api/create-account', create_account_view),
    path('api/login', login_user_view),
    path('api/account-list', account_list_view),
    path('api/campaigns/<int:customer_id>', get_campaign_for_customer_view),
    path('api/adgroups/<int:customer_id>/<int:campaign_id>', get_adgroups_for_customer_view),
    path('api/customer/<int:customer_id>/adgroup/<int:ad_group_id>', get_search_ads_view),
    path('api/add-adgroup', add_adgroups_view),
    path('api/dynamic-search-adgroup/<int:customer_id>', ad_group_for_responsive_search_ads_view),
    path('api/responsive-search-ad', responsive_search_ad_view),
    path('api/excel-manage-ads', excel_sheet_to_create_google_ads_view),
    path('api/excel-ads-template', template_for_excel_ads_with_io_view)
]