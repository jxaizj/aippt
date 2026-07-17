# settings_app - stores app settings
from django.db import models


class AppSetting(models.Model):
    """应用设置键值存储"""
    key = models.CharField(max_length=100, primary_key=True, verbose_name='设置键')
    value = models.TextField(verbose_name='设置值')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'app_settings'
        verbose_name = '应用设置'
        verbose_name_plural = '应用设置'

    def __str__(self):
        return self.key


class UserPreference(models.Model):
    """用户偏好（AI学习）"""
    key = models.CharField(max_length=100, primary_key=True, verbose_name='偏好键')
    value = models.TextField(verbose_name='偏好值')
    confidence = models.FloatField(default=1.0, verbose_name='置信度')
    source_sessions = models.JSONField(default=list, blank=True, verbose_name='来源会话')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    last_used_at = models.DateTimeField(null=True, blank=True, verbose_name='最后使用时间')

    class Meta:
        db_table = 'user_preferences'
        verbose_name = '用户偏好'
        verbose_name_plural = '用户偏好'

    def __str__(self):
        return self.key


class ModelUsageEvent(models.Model):
    """模型使用统计"""
    id = models.UUIDField(primary_key=True, editable=False)
    provider = models.CharField(max_length=50, verbose_name='提供商')
    model = models.CharField(max_length=100, verbose_name='模型')
    model_config = models.ForeignKey('ppt_sessions.ModelConfig', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='模型配置')
    input_tokens = models.IntegerField(default=0, verbose_name='输入Token')
    output_tokens = models.IntegerField(default=0, verbose_name='输出Token')
    total_tokens = models.IntegerField(default=0, verbose_name='总Token')
    usage_source = models.CharField(max_length=20, default='provider', verbose_name='用量来源')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'model_usage_events'
        ordering = ['-created_at']
        verbose_name = '模型使用记录'
        verbose_name_plural = '模型使用记录'
        indexes = [
            models.Index(fields=['created_at'], name='idx_model_usage_created'),
            models.Index(fields=['provider', 'model', 'created_at'], name='idx_model_usage_model'),
        ]

    def __str__(self):
        return f'{self.provider}/{self.model} - {self.total_tokens}tokens'
