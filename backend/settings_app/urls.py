from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'settings', views.AppSettingViewSet, basename='app-setting')

urlpatterns = [
    path('', include(router.urls)),
    path('all/', views.get_settings, name='settings-all'),
    path('update/', views.update_setting, name='settings-update'),
    path('update-batch/', views.update_settings_batch, name='settings-update-batch'),
    path('verify-api-key/', views.verify_api_key, name='settings-verify-api-key'),
    path('preferences/', views.get_preferences, name='settings-preferences'),
    path('preferences/update/', views.update_preference, name='settings-preference-update'),
    path('model-usage/', views.get_model_usage, name='settings-model-usage'),
    path('model-usage/record/', views.record_model_usage, name='settings-model-usage-record'),
]
