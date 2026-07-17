from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import AppSetting, UserPreference, ModelUsageEvent

# 默认超时配置（毫秒）
DEFAULT_TIMEOUTS = {
    'planning': 300000,   # 5 min
    'design': 300000,     # 5 min
    'agent': 600000,      # 10 min
    'document': 600000,   # 10 min
}


@api_view(['GET'])
def get_settings(request):
    """获取所有设置（包含超时配置）"""
    settings = AppSetting.objects.all()
    result = {s.key: s.value for s in settings}

    # 构建超时配置对象
    timeouts = {}
    for profile in ['planning', 'design', 'agent', 'document']:
        key = f'timeout_ms_{profile}'
        try:
            timeouts[profile] = int(result.get(key, DEFAULT_TIMEOUTS[profile]))
        except (ValueError, TypeError):
            timeouts[profile] = DEFAULT_TIMEOUTS[profile]

    # 解析 JSON 值
    for key, value in result.items():
        if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
            try:
                import json
                result[key] = json.loads(value)
            except (json.JSONDecodeError, ValueError):
                pass

    result['timeouts'] = timeouts
    return Response(result)


@api_view(['POST'])
def update_setting(request):
    """更新设置"""
    key = request.data.get('key')
    value = request.data.get('value', '')

    # 处理超时配置
    if key.startswith('timeout_ms_'):
        try:
            value = str(int(value))
        except (ValueError, TypeError):
            return Response({'error': '无效的超时值'}, status=400)

    # 处理 JSON 值（如主题、locale）
    if isinstance(value, str) and key in ('theme', 'locale'):
        import json
        value = json.dumps(value)

    setting, created = AppSetting.objects.update_or_create(
        key=key, defaults={'value': value}
    )
    return Response({'key': key, 'value': value, 'created': created})


@api_view(['POST'])
def update_settings_batch(request):
    """批量更新设置"""
    settings = request.data.get('settings', {})
    if isinstance(settings, dict):
        for key, value in settings.items():
            if key.startswith('timeout_ms_'):
                try:
                    value = str(int(value))
                except (ValueError, TypeError):
                    continue
            elif key in ('theme', 'locale'):
                import json
                value = json.dumps(value)
            AppSetting.objects.update_or_create(key=key, defaults={'value': value})
    return Response({'status': 'ok'})


@api_view(['POST'])
def verify_api_key(request):
    """验证 API Key 是否可用"""
    provider = request.data.get('provider', 'openai')
    api_key = request.data.get('api_key', '')
    model = request.data.get('model', '')
    base_url = request.data.get('base_url', '')

    if not api_key:
        return Response({'valid': False, 'message': '请先填写 api_key'})
    if not model:
        return Response({'valid': False, 'message': '请先填写 model'})

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url=base_url or None)
        client.chat.completions.create(
            model=model,
            messages=[{'role': 'user', 'content': 'Reply with OK.'}],
            max_tokens=5,
        )
        return Response({'valid': True, 'message': '连接验证成功'})
    except Exception as e:
        return Response({'valid': False, 'message': str(e)})


@api_view(['GET'])
def get_preferences(request):
    prefs = UserPreference.objects.all()
    result = {p.key: {'value': p.value, 'confidence': p.confidence} for p in prefs}
    return Response(result)


@api_view(['POST'])
def update_preference(request):
    key = request.data.get('key')
    value = request.data.get('value', '')
    pref, created = UserPreference.objects.update_or_create(
        key=key, defaults={'value': value}
    )
    return Response({'key': key, 'value': value, 'created': created})


@api_view(['GET'])
def get_model_usage(request):
    events = ModelUsageEvent.objects.all().order_by('-created_at')[:100]
    result = [{
        'id': str(e.id),
        'provider': e.provider,
        'model': e.model,
        'input_tokens': e.input_tokens,
        'output_tokens': e.output_tokens,
        'total_tokens': e.total_tokens,
        'created_at': e.created_at.isoformat(),
    } for e in events]
    return Response(result)


@api_view(['POST'])
def record_model_usage(request):
    import uuid
    event = ModelUsageEvent.objects.create(
        id=uuid.uuid4(),
        provider=request.data.get('provider', ''),
        model=request.data.get('model', ''),
        input_tokens=request.data.get('input_tokens', 0),
        output_tokens=request.data.get('output_tokens', 0),
        total_tokens=request.data.get('total_tokens', 0),
        usage_source=request.data.get('usage_source', 'provider'),
    )
    return Response({'id': str(event.id), 'status': 'recorded'})


class AppSettingViewSet(viewsets.ModelViewSet):
    queryset = AppSetting.objects.all()

    def get_serializer_class(self):
        from rest_framework import serializers
        class SettingSerializer(serializers.ModelSerializer):
            class Meta:
                model = AppSetting
                fields = '__all__'
        return SettingSerializer
