import json
import os
import re
from django.conf import settings


def get_active_provider():
    """获取当前激活的 AI 模型配置（ModelConfig）"""
    from sessions.models import ModelConfig
    return ModelConfig.objects.filter(active=True).first()


def get_openai_client(provider=None):
    from openai import OpenAI
    if provider is None:
        provider = get_active_provider()
    if not provider:
        return None
    return OpenAI(api_key=provider.api_key, base_url=provider.base_url or None)


def save_uploaded_file(file, subdir):
    upload_dir = os.path.join(settings.OHMYPPT_STORAGE_ROOT, subdir)
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.name)
    with open(file_path, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)
    return file_path


def safe_json_parse(content, pattern=r'\[.*\]', default=None):
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            return json.loads(match.group())
    return default if default is not None else ([] if pattern.startswith(r'\[') else {})