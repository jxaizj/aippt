from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/sessions/', include('sessions.urls')),
    path('api/settings/', include('settings_app.urls')),
    path('api/editor/', include('editor.urls')),
    path('api/export/', include('export_app.urls')),
    path('api/ai/', include('ai_engine.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
