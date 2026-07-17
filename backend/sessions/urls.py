from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SessionViewSet, MessageViewSet, SessionPageViewSet,
    StyleViewSet, TemplateViewSet,
    ModelConfigViewSet, ImageModelConfigViewSet,
    SessionOperationViewSet, GenerationRunViewSet, GenerationPageViewSet,
    FontViewSet, ImageAssetViewSet, SpeechScriptViewSet
)

app_name = 'ppt_sessions'

router = DefaultRouter()
# 注册具体路由在前，空前缀在后，避免 pk 模式匹配到子路由
router.register(r'styles', StyleViewSet, basename='style')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'pages', SessionPageViewSet, basename='session-page')
router.register(r'templates', TemplateViewSet, basename='template')
router.register(r'model-configs', ModelConfigViewSet, basename='model-config')
router.register(r'image-model-configs', ImageModelConfigViewSet, basename='image-model-config')
router.register(r'operations', SessionOperationViewSet, basename='session-operation')
router.register(r'generation-runs', GenerationRunViewSet, basename='generation-run')
router.register(r'generation-pages', GenerationPageViewSet, basename='generation-page')
router.register(r'fonts', FontViewSet, basename='font')
router.register(r'images', ImageAssetViewSet, basename='image-asset')
router.register(r'speeches', SpeechScriptViewSet, basename='speech')
router.register(r'', SessionViewSet, basename='session')

urlpatterns = [
    path('', include((router.urls, 'ppt_sessions'))),
]
