from rest_framework import serializers
from .models import (
    Session, Message, SessionPage, Style, Template,
    ModelConfig, ImageModelConfig, SessionOperation,
    GenerationRun, GenerationPage, Font, ImageAsset, SpeechScript
)


class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class SessionPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionPage
        fields = '__all__'


class SessionPageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionPage
        fields = ['id', 'page_number', 'title', 'status', 'html_content', 'created_at', 'updated_at']


class SessionSerializer(serializers.ModelSerializer):
    style_detail = StyleSerializer(source='style', read_only=True)
    page_count_actual = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = '__all__'

    def get_page_count_actual(self, obj):
        return obj.pages.filter(deleted_at__isnull=True).count()


class SessionListSerializer(serializers.ModelSerializer):
    style_name = serializers.CharField(source='style.style_name', read_only=True)
    page_count_actual = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = ['id', 'title', 'topic', 'status', 'slide_size', 'slide_width',
                  'slide_height', 'provider', 'model', 'style_name', 'page_count',
                  'page_count_actual', 'created_at', 'updated_at']

    def get_page_count_actual(self, obj):
        return obj.pages.filter(deleted_at__isnull=True).count()


class SessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'title', 'topic', 'page_count', 'slide_size', 'slide_width',
                  'slide_height', 'provider', 'model', 'style', 'reference_document_path']


class TemplateSerializer(serializers.ModelSerializer):
    style_detail = StyleSerializer(source='style', read_only=True)
    session_title = serializers.CharField(source='session.title', read_only=True)

    class Meta:
        model = Template
        fields = '__all__'


class ModelConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelConfig
        fields = '__all__'


class ImageModelConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModelConfig
        fields = '__all__'


class SessionOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionOperation
        fields = '__all__'


class GenerationRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenerationRun
        fields = '__all__'


class GenerationPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenerationPage
        fields = '__all__'


class FontSerializer(serializers.ModelSerializer):
    class Meta:
        model = Font
        fields = '__all__'


class ImageAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageAsset
        fields = '__all__'


class SpeechScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeechScript
        fields = '__all__'
