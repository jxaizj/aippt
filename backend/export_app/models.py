# export app
from django.db import models
import uuid


class ExportTask(models.Model):
    """导出任务"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey('ppt_sessions.Session', on_delete=models.CASCADE, related_name='exports', verbose_name='会话')

    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('png', 'PNG'),
        ('png-long', 'PNG长图'),
        ('pptx', 'PPTX'),
        ('mp4', 'MP4'),
        ('html', 'HTML打包'),
    ]
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, verbose_name='导出格式')

    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('completed', '已完成'),
        ('failed', '失败'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='状态')

    output_path = models.CharField(max_length=500, blank=True, verbose_name='输出路径')
    file_size = models.IntegerField(default=0, verbose_name='文件大小')
    error = models.TextField(blank=True, null=True, verbose_name='错误信息')
    progress = models.IntegerField(default=0, verbose_name='进度')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')

    class Meta:
        db_table = 'export_tasks'
        ordering = ['-created_at']
        verbose_name = '导出任务'
        verbose_name_plural = '导出任务'

    def __str__(self):
        return f'{self.get_format_display()} - {self.session.title}'
