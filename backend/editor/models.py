# editor app - page editing operations
from django.db import models
import uuid


class PageEdit(models.Model):
    """页面编辑记录"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    page = models.ForeignKey('ppt_sessions.SessionPage', on_delete=models.CASCADE, related_name='edits', verbose_name='页面')
    operation = models.ForeignKey('ppt_sessions.SessionOperation', on_delete=models.CASCADE, related_name='page_edits', verbose_name='操作')

    # 编辑内容
    element_selector = models.CharField(max_length=255, blank=True, verbose_name='元素选择器')
    action = models.CharField(max_length=50, verbose_name='操作类型')  # add, remove, modify, move, resize
    before_state = models.JSONField(default=dict, blank=True, verbose_name='编辑前状态')
    after_state = models.JSONField(default=dict, blank=True, verbose_name='编辑后状态')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'page_edits'
        ordering = ['created_at']
        verbose_name = '页面编辑'
        verbose_name_plural = '页面编辑'

    def __str__(self):
        return f'{self.action} - {self.page}'


class ElementAnimation(models.Model):
    """元素动画配置"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    page = models.ForeignKey('ppt_sessions.SessionPage', on_delete=models.CASCADE, related_name='animations', verbose_name='页面')
    element_selector = models.CharField(max_length=255, verbose_name='元素选择器')

    ANIMATION_TYPE_CHOICES = [
        ('entrance', '入场'),
        ('emphasis', '强调'),
        ('exit', '退出'),
    ]
    animation_type = models.CharField(max_length=10, choices=ANIMATION_TYPE_CHOICES, verbose_name='动画类型')

    EFFECT_CHOICES = [
        ('fadeIn', '淡入'),
        ('fadeInUp', '上移入'),
        ('fadeInDown', '下移入'),
        ('fadeInLeft', '左移入'),
        ('fadeInRight', '右移入'),
        ('zoomIn', '放大'),
        ('zoomOut', '缩小'),
        ('bounceIn', '弹入'),
        ('slideInUp', '上滑入'),
        ('slideInDown', '下滑入'),
        ('slideInLeft', '左滑入'),
        ('slideInRight', '右滑入'),
        ('rotateIn', '旋转入'),
        ('flipInX', 'X轴翻转'),
        ('flipInY', 'Y轴翻转'),
    ]
    effect = models.CharField(max_length=20, choices=EFFECT_CHOICES, default='fadeIn', verbose_name='效果')

    TRIGGER_CHOICES = [
        ('auto', '自动'),
        ('click', '点击'),
        ('sequential', '顺序'),
    ]
    trigger = models.CharField(max_length=10, choices=TRIGGER_CHOICES, default='auto', verbose_name='触发方式')

    duration = models.IntegerField(default=600, verbose_name='时长(ms)')
    delay = models.IntegerField(default=0, verbose_name='延迟(ms)')
    order = models.IntegerField(default=0, verbose_name='顺序')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'element_animations'
        ordering = ['order']
        verbose_name = '元素动画'
        verbose_name_plural = '元素动画'

    def __str__(self):
        return f'{self.get_animation_type_display()} - {self.get_effect_display()}'
