import json
from django.db import migrations


def load_settings(apps, schema_editor):
    AppSetting = apps.get_model('settings_app', 'AppSetting')
    settings_data = [["theme", "light"], ["locale", "zh"], ["timeout_ms_planning", "300000"], ["timeout_ms_design", "300000"], ["timeout_ms_agent", "600000"], ["timeout_ms_document", "600000"], ["proxy_url", ""]]
    
    for key, value in settings_data:
        AppSetting.objects.get_or_create(key=key, defaults={'value': value})


def unload_settings(apps, schema_editor):
    AppSetting = apps.get_model('settings_app', 'AppSetting')
    AppSetting.objects.filter(key__in=[s[0] for s in [
        ('theme',), ('locale',), ('timeout_ms_planning',), ('timeout_ms_design',),
        ('timeout_ms_agent',), ('timeout_ms_document',), ('proxy_url',)
    ]]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('settings_app', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(load_settings, unload_settings),
    ]
