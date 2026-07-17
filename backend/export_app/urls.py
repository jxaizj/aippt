from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tasks', views.ExportTaskViewSet, basename='export-task')

urlpatterns = [
    path('', include(router.urls)),
    path('pdf/', views.export_pdf, name='export-pdf'),
    path('png/', views.export_png, name='export-png'),
    path('pptx/', views.export_pptx, name='export-pptx'),
    path('mp4/', views.export_mp4, name='export-mp4'),
    path('html/', views.export_html, name='export-html'),
    path('download/<uuid:task_id>/', views.download_export, name='export-download'),
]
