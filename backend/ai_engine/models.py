# ai_engine app
from django.db import models
import uuid


class AIConversation(models.Model):
    """AI对话（多轮思考）"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey('ppt_sessions.Session', on_delete=models.CASCADE, related_name='ai_conversations', verbose_name='会话')
    task_type = models.CharField(max_length=50, verbose_name='任务类型')  # generate, edit, speech, outline
    messages = models.JSONField(default=list, verbose_name='消息列表')

    STATUS_CHOICES = [
        ('running', '运行中'),
        ('completed', '已完成'),
        ('failed', '失败'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='running', verbose_name='状态')

    result = models.JSONField(default=dict, blank=True, verbose_name='结果')
    error = models.TextField(blank=True, null=True, verbose_name='错误信息')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'ai_conversations'
        ordering = ['-created_at']
        verbose_name = 'AI对话'
        verbose_name_plural = 'AI对话'

    def __str__(self):
        return f'{self.task_type} - {self.session.title}'
