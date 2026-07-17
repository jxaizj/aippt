from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import (
    Session, Message, SessionPage, Style, Template,
    ModelConfig, ImageModelConfig, SessionOperation,
    GenerationRun, GenerationPage, Font, ImageAsset, SpeechScript
)
from .serializers import (
    SessionSerializer, SessionListSerializer, SessionCreateSerializer,
    MessageSerializer, SessionPageSerializer,
    StyleSerializer, TemplateSerializer,
    ModelConfigSerializer, ImageModelConfigSerializer,
    SessionOperationSerializer, GenerationRunSerializer, GenerationPageSerializer,
    FontSerializer, ImageAssetSerializer, SpeechScriptSerializer
)


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return SessionListSerializer
        if self.action == 'create':
            return SessionCreateSerializer
        return SessionSerializer

    def perform_create(self, serializer):
        session = serializer.save()
        for i in range(1, (session.page_count or 10) + 1):
            SessionPage.objects.create(
                session=session,
                file_slug=f'page-{i}',
                page_number=i,
                title=f'第{i}页',
                html_path=f'/sessions/{session.id}/pages/page-{i}.html',
                status='pending'
            )

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        session = self.get_object()
        messages = session.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def pages(self, request, pk=None):
        session = self.get_object()
        pages = session.pages.filter(deleted_at__isnull=True)
        serializer = SessionPageSerializer(pages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def operations(self, request, pk=None):
        session = self.get_object()
        operations = session.operations.all()
        serializer = SessionOperationSerializer(operations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def speeches(self, request, pk=None):
        session = self.get_object()
        speeches = session.speeches.all()
        serializer = SpeechScriptSerializer(speeches, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        session = self.get_object()
        new_session = Session.objects.create(
            title=f'{session.title} (副本)',
            topic=session.topic,
            page_count=session.page_count,
            slide_size=session.slide_size,
            slide_width=session.slide_width,
            slide_height=session.slide_height,
            provider=session.provider,
            model=session.model,
            style=session.style,
            design_contract=session.design_contract,
        )
        for page in session.pages.filter(deleted_at__isnull=True):
            SessionPage.objects.create(
                session=new_session,
                file_slug=page.file_slug,
                page_number=page.page_number,
                title=page.title,
                html_path=page.html_path,
                html_content=page.html_content,
                status='pending'
            )
        return Response(SessionSerializer(new_session).data)

    @action(detail=True, methods=['post'])
    def save_as_template(self, request, pk=None):
        session = self.get_object()
        title = request.data.get('title', f'{session.title} 模板')
        template = Template.objects.create(
            title=title,
            description=request.data.get('description', ''),
            session=session,
            style=session.style,
            slide_size=session.slide_size,
            slide_width=session.slide_width,
            slide_height=session.slide_height,
            design_contract=session.design_contract,
            source='session',
        )
        return Response(TemplateSerializer(template).data)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filterset_fields = ['session', 'role', 'chat_scope']


class SessionPageViewSet(viewsets.ModelViewSet):
    queryset = SessionPage.objects.filter(deleted_at__isnull=True)
    serializer_class = SessionPageSerializer
    filterset_fields = ['session', 'status']

    @action(detail=True, methods=['post'])
    def update_content(self, request, pk=None):
        page = self.get_object()
        html_content = request.data.get('html_content', '')
        page.html_content = html_content
        page.status = 'completed'
        page.save()
        return Response(SessionPageSerializer(page).data)


class StyleViewSet(viewsets.ModelViewSet):
    queryset = Style.objects.filter(active=True).order_by('source', 'category', 'style_name')
    serializer_class = StyleSerializer

    @action(detail=True, methods=['post'])
    def toggle_favorite(self, request, pk=None):
        from django.utils import timezone
        style = self.get_object()
        style.favorite_at = None if style.favorite_at else timezone.now()
        style.save()
        return Response(StyleSerializer(style).data)


class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.filter(active=True)
    serializer_class = TemplateSerializer

    @action(detail=True, methods=['post'])
    def create_session(self, request, pk=None):
        template = self.get_object()
        title = request.data.get('title', template.title)
        topic = request.data.get('topic', '')
        session = Session.objects.create(
            title=title,
            topic=topic,
            page_count=10,
            slide_size=template.slide_size,
            slide_width=template.slide_width,
            slide_height=template.slide_height,
            style=template.style,
            design_contract=template.design_contract,
        )
        return Response(SessionSerializer(session).data)


class ModelConfigViewSet(viewsets.ModelViewSet):
    queryset = ModelConfig.objects.all()
    serializer_class = ModelConfigSerializer

    @action(detail=True, methods=['post'])
    def set_active(self, request, pk=None):
        config = self.get_object()
        ModelConfig.objects.all().update(active=False)
        config.active = True
        config.save()
        return Response(ModelConfigSerializer(config).data)


class ImageModelConfigViewSet(viewsets.ModelViewSet):
    queryset = ImageModelConfig.objects.all()
    serializer_class = ImageModelConfigSerializer


class SessionOperationViewSet(viewsets.ModelViewSet):
    queryset = SessionOperation.objects.all()
    serializer_class = SessionOperationSerializer
    filterset_fields = ['session', 'type', 'status']


class GenerationRunViewSet(viewsets.ModelViewSet):
    queryset = GenerationRun.objects.all()
    serializer_class = GenerationRunSerializer
    filterset_fields = ['session', 'status', 'mode']


class GenerationPageViewSet(viewsets.ModelViewSet):
    queryset = GenerationPage.objects.all()
    serializer_class = GenerationPageSerializer
    filterset_fields = ['session', 'run', 'status']


class FontViewSet(viewsets.ModelViewSet):
    queryset = Font.objects.filter(active=True)
    serializer_class = FontSerializer


class ImageAssetViewSet(viewsets.ModelViewSet):
    queryset = ImageAsset.objects.all()
    serializer_class = ImageAssetSerializer
    filterset_fields = ['session']


class SpeechScriptViewSet(viewsets.ModelViewSet):
    queryset = SpeechScript.objects.all()
    serializer_class = SpeechScriptSerializer
    filterset_fields = ['session', 'page', 'style']
