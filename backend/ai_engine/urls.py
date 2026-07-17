from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'conversations', views.AIConversationViewSet, basename='ai-conversation')

urlpatterns = [
    path('', include(router.urls)),
    path('generate/', views.generate_ppt, name='ai-generate'),
    path('chat-edit/', views.chat_edit, name='ai-chat-edit'),
    path('generate-speech/', views.generate_speech, name='ai-generate-speech'),
    path('generate-outline/', views.generate_outline, name='ai-generate-outline'),
    path('upload-document/', views.upload_document, name='ai-upload-document'),
    path('import-pptx/', views.import_pptx, name='ai-import-pptx'),
    path('analyze-image/', views.analyze_image, name='ai-analyze-image'),
]
