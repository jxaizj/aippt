import uuid
from django.db import models


class Session(models.Model):
    """演示文稿会话"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name='标题')
    topic = models.TextField(blank=True, null=True, verbose_name='主题')
    style = models.ForeignKey('Style', on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions', verbose_name='风格')
    page_count = models.IntegerField(default=10, verbose_name='页数')

    SLIDE_SIZE_CHOICES = [
        ('wide-16-9', '16:9 宽屏'),
        ('standard-4-3', '4:3 标准'),
        ('vertical-9-16', '9:16 竖屏'),
        ('vertical-3-4', '3:4 竖版'),
        ('square-1-1', '1:1 方图'),
        ('a4-portrait', 'A4 竖版'),
        ('a4-landscape', 'A4 横版'),
    ]
    slide_size = models.CharField(max_length=20, choices=SLIDE_SIZE_CHOICES, default='wide-16-9', verbose_name='画布尺寸')
    slide_width = models.IntegerField(default=1600, verbose_name='画布宽度')
    slide_height = models.IntegerField(default=900, verbose_name='画布高度')

    reference_document_path = models.CharField(max_length=500, blank=True, null=True, verbose_name='参考文档路径')

    STATUS_CHOICES = [
        ('active', '活跃'),
        ('completed', '已完成'),
        ('failed', '失败'),
        ('archived', '已归档'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='状态')

    provider = models.CharField(max_length=50, default='openai', verbose_name='AI提供商')
    model = models.CharField(max_length=100, default='gpt-4', verbose_name='AI模型')

    design_contract = models.JSONField(default=dict, blank=True, verbose_name='设计合同')
    current_operation = models.ForeignKey('SessionOperation', on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name='当前操作')
    current_commit = models.CharField(max_length=64, blank=True, null=True, verbose_name='当前提交哈希')
    metadata = models.JSONField(default=dict, blank=True, verbose_name='元数据')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'sessions'
        ordering = ['-updated_at']
        verbose_name = '会话'
        verbose_name_plural = '会话'

    def __str__(self):
        return self.title


class Message(models.Model):
    """会话消息（对话历史）"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='messages', verbose_name='会话')

    CHAT_SCOPE_CHOICES = [
        ('main', '主对话'),
        ('page', '页面对话'),
    ]
    chat_scope = models.CharField(max_length=10, choices=CHAT_SCOPE_CHOICES, default='main', verbose_name='对话范围')
    page = models.ForeignKey('SessionPage', on_delete=models.SET_NULL, null=True, blank=True, related_name='messages', verbose_name='关联页面')
    selector = models.CharField(max_length=255, blank=True, null=True, verbose_name='元素选择器')

    image_paths = models.JSONField(default=list, blank=True, verbose_name='图片路径')
    video_paths = models.JSONField(default=list, blank=True, verbose_name='视频路径')

    ROLE_CHOICES = [
        ('user', '用户'),
        ('assistant', '助手'),
        ('system', '系统'),
        ('tool', '工具'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, verbose_name='角色')
    content = models.TextField(verbose_name='内容')

    TYPE_CHOICES = [
        ('text', '文本'),
        ('tool_call', '工具调用'),
        ('tool_result', '工具结果'),
        ('stream_chunk', '流式片段'),
    ]
    type = models.CharField(max_length=15, choices=TYPE_CHOICES, default='text', verbose_name='类型')
    tool_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='工具名称')
    tool_call_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='工具调用ID')

    token_count = models.IntegerField(null=True, blank=True, verbose_name='Token数量')
    run_model = models.CharField(max_length=100, blank=True, null=True, verbose_name='运行模型')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'messages'
        ordering = ['created_at']
        verbose_name = '消息'
        verbose_name_plural = '消息'

    def __str__(self):
        return f'{self.role}: {self.content[:50]}'


class SessionPage(models.Model):
    """会话页面（幻灯片）"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='pages', verbose_name='会话')
    file_slug = models.CharField(max_length=100, verbose_name='文件标识')
    page_number = models.IntegerField(verbose_name='页码')
    title = models.CharField(max_length=255, verbose_name='页面标题')
    html_path = models.CharField(max_length=500, verbose_name='HTML文件路径')
    html_content = models.TextField(blank=True, verbose_name='HTML内容')

    STATUS_CHOICES = [
        ('pending', '待生成'),
        ('completed', '已完成'),
        ('failed', '失败'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    error = models.TextField(blank=True, null=True, verbose_name='错误信息')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='删除时间')

    class Meta:
        db_table = 'session_pages'
        ordering = ['page_number']
        verbose_name = '会话页面'
        verbose_name_plural = '会话页面'

    def __str__(self):
        return f'{self.session.title} - 第{self.page_number}页'


class Style(models.Model):
    """风格/样式配置"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    style = models.CharField(max_length=100, unique=True, verbose_name='风格标识')
    style_name = models.CharField(max_length=100, verbose_name='风格名称')
    style_name_zh = models.CharField(max_length=100, blank=True, verbose_name='中文名')
    style_name_en = models.CharField(max_length=100, blank=True, verbose_name='英文名')
    description = models.TextField(blank=True, verbose_name='描述')
    category = models.CharField(max_length=50, blank=True, verbose_name='分类')
    aliases = models.JSONField(default=list, blank=True, verbose_name='别名')
    source = models.CharField(max_length=20, default='custom', verbose_name='来源')
    style_skill = models.TextField(blank=True, verbose_name='风格技能')
    version = models.CharField(max_length=20, default='1.0.0', verbose_name='版本')
    style_case = models.TextField(blank=True, verbose_name='风格案例')
    package_dir = models.CharField(max_length=255, blank=True, verbose_name='包目录')
    active = models.BooleanField(default=True, verbose_name='启用')
    favorite_at = models.DateTimeField(null=True, blank=True, verbose_name='收藏时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'styles'
        ordering = ['-favorite_at', '-created_at']
        verbose_name = '风格'
        verbose_name_plural = '风格'

    def __str__(self):
        return self.style_name


class Template(models.Model):
    """模板"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name='模板标题')
    description = models.TextField(blank=True, verbose_name='描述')
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True, blank=True, related_name='templates', verbose_name='源会话')
    style = models.ForeignKey(Style, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='风格')

    thumbnail_path = models.CharField(max_length=500, blank=True, verbose_name='缩略图路径')
    template_dir = models.CharField(max_length=500, blank=True, verbose_name='模板目录')
    design_contract = models.JSONField(default=dict, blank=True, verbose_name='设计合同')

    slide_size = models.CharField(max_length=20, default='wide-16-9', verbose_name='画布尺寸')
    slide_width = models.IntegerField(default=1600, verbose_name='画布宽度')
    slide_height = models.IntegerField(default=900, verbose_name='画布高度')

    SOURCE_CHOICES = [
        ('session', '会话'),
        ('pptx', 'PPTX导入'),
        ('manual', '手动创建'),
    ]
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES, default='session', verbose_name='来源')

    active = models.BooleanField(default=True, verbose_name='启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'templates'
        ordering = ['-created_at']
        verbose_name = '模板'
        verbose_name_plural = '模板'

    def __str__(self):
        return self.title


class ModelConfig(models.Model):
    """AI模型配置"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name='配置名称')
    provider = models.CharField(max_length=50, verbose_name='提供商')
    model = models.CharField(max_length=100, verbose_name='模型名称')
    api_key = models.CharField(max_length=255, blank=True, verbose_name='API Key')
    base_url = models.CharField(max_length=255, blank=True, verbose_name='Base URL')
    max_tokens = models.IntegerField(default=4096, verbose_name='最大Token数')
    disable_temperature = models.BooleanField(default=False, verbose_name='禁用温度参数')

    THINKING_MODE_CHOICES = [
        ('auto', '自动'),
        ('off', '关闭'),
        ('on', '开启'),
    ]
    thinking_parameter_mode = models.CharField(max_length=10, choices=THINKING_MODE_CHOICES, default='auto', verbose_name='思考参数模式')

    active = models.BooleanField(default=False, verbose_name='启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'model_configs'
        ordering = ['-active', '-created_at']
        verbose_name = '模型配置'
        verbose_name_plural = '模型配置'

    def __str__(self):
        return self.name


class ImageModelConfig(models.Model):
    """图片生成模型配置"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name='配置名称')
    provider = models.CharField(max_length=50, verbose_name='提供商')
    model_config = models.JSONField(default=dict, verbose_name='模型配置')
    active = models.BooleanField(default=False, verbose_name='启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'image_model_configs'
        ordering = ['-active', '-created_at']
        verbose_name = '图片模型配置'
        verbose_name_plural = '图片模型配置'

    def __str__(self):
        return self.name


class SessionOperation(models.Model):
    """会话操作记录（撤销/重做/版本回退）"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='operations', verbose_name='会话')

    TYPE_CHOICES = [
        ('generate', '生成'),
        ('edit', '编辑'),
        ('addPage', '添加页面'),
        ('retry', '重试'),
        ('import', '导入'),
        ('rollback', '回退'),
        ('reorder', '重排序'),
        ('delete', '删除'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name='操作类型')

    STATUS_CHOICES = [
        ('committing', '提交中'),
        ('completed', '已完成'),
        ('failed', '失败'),
        ('noop', '无操作'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='completed', verbose_name='状态')

    SCOPE_CHOICES = [
        ('session', '会话'),
        ('deck', '演示文稿'),
        ('page', '页面'),
        ('selector', '选择器'),
        ('shell', 'Shell'),
    ]
    scope = models.CharField(max_length=10, choices=SCOPE_CHOICES, blank=True, null=True, verbose_name='范围')

    prompt = models.TextField(blank=True, null=True, verbose_name='提示词')
    parent_operation = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='child_operations', verbose_name='父操作')

    before_commit = models.CharField(max_length=64, blank=True, null=True, verbose_name='操作前提交')
    after_commit = models.CharField(max_length=64, blank=True, null=True, verbose_name='操作后提交')
    target_operation = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name='目标操作')
    target_commit = models.CharField(max_length=64, blank=True, null=True, verbose_name='目标提交')

    changed_files = models.JSONField(default=list, blank=True, verbose_name='变更文件')
    changed_pages = models.JSONField(default=list, blank=True, verbose_name='变更页面')
    tracked_files = models.JSONField(default=list, blank=True, verbose_name='跟踪文件')
    metadata = models.JSONField(default=dict, blank=True, verbose_name='元数据')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')

    class Meta:
        db_table = 'session_operations'
        ordering = ['-created_at']
        verbose_name = '会话操作'
        verbose_name_plural = '会话操作'

    def __str__(self):
        return f'{self.get_type_display()} - {self.session.title}'


class GenerationRun(models.Model):
    """生成运行记录"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='generation_runs', verbose_name='会话')

    MODE_CHOICES = [
        ('generate', '生成'),
        ('retry', '重试'),
        ('edit', '编辑'),
        ('import', '导入'),
        ('addPage', '添加页面'),
        ('retrySinglePage', '重试单页'),
    ]
    mode = models.CharField(max_length=15, choices=MODE_CHOICES, default='generate', verbose_name='模式')

    STATUS_CHOICES = [
        ('running', '运行中'),
        ('completed', '已完成'),
        ('failed', '失败'),
        ('partial', '部分完成'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='running', verbose_name='状态')

    total_pages = models.IntegerField(default=0, verbose_name='总页数')
    error = models.TextField(blank=True, null=True, verbose_name='错误信息')
    metadata = models.JSONField(default=dict, blank=True, verbose_name='元数据')
    animation_preferences = models.JSONField(default=dict, blank=True, verbose_name='动画偏好')
    model_config = models.ForeignKey(ModelConfig, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='模型配置')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'generation_runs'
        ordering = ['-created_at']
        verbose_name = '生成运行'
        verbose_name_plural = '生成运行'

    def __str__(self):
        return f'{self.get_mode_display()} - {self.session.title}'


class GenerationPage(models.Model):
    """生成页面记录"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    run = models.ForeignKey(GenerationRun, on_delete=models.CASCADE, related_name='pages', verbose_name='生成运行')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='generation_pages', verbose_name='会话')
    page_id = models.CharField(max_length=100, verbose_name='页面ID')
    page_number = models.IntegerField(verbose_name='页码')
    title = models.CharField(max_length=255, verbose_name='标题')
    content_outline = models.TextField(blank=True, null=True, verbose_name='内容大纲')
    layout_intent = models.JSONField(default=dict, blank=True, verbose_name='布局意图')
    html_path = models.CharField(max_length=500, blank=True, null=True, verbose_name='HTML路径')

    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('running', '运行中'),
        ('completed', '已完成'),
        ('failed', '失败'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    error = models.TextField(blank=True, null=True, verbose_name='错误信息')
    retry_count = models.IntegerField(default=0, verbose_name='重试次数')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'generation_pages'
        ordering = ['page_number']
        verbose_name = '生成页面'
        verbose_name_plural = '生成页面'

    def __str__(self):
        return f'第{self.page_number}页 - {self.title}'


class Font(models.Model):
    """字体管理"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name='字体名称')
    display_name = models.CharField(max_length=100, verbose_name='显示名称')

    CATEGORY_CHOICES = [
        ('sans-serif', '无衬线'),
        ('serif', '衬线'),
        ('handwriting', '手写'),
        ('monospace', '等宽'),
        ('display', '展示'),
    ]
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES, default='sans-serif', verbose_name='分类')

    USAGE_CHOICES = [
        ('title', '标题'),
        ('body', '正文'),
        ('both', '通用'),
    ]
    usage = models.CharField(max_length=10, choices=USAGE_CHOICES, default='both', verbose_name='用途')

    LANG_CHOICES = [
        ('latin', '拉丁'),
        ('cjk', '中日韩'),
        ('all', '全部'),
    ]
    language = models.CharField(max_length=10, choices=LANG_CHOICES, default='all', verbose_name='语言')

    file_path = models.CharField(max_length=500, blank=True, verbose_name='文件路径')
    is_system = models.BooleanField(default=False, verbose_name='系统字体')
    active = models.BooleanField(default=True, verbose_name='启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'fonts'
        ordering = ['category', 'name']
        verbose_name = '字体'
        verbose_name_plural = '字体'

    def __str__(self):
        return self.display_name


class ImageAsset(models.Model):
    """图片素材"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='images', verbose_name='会话', null=True, blank=True)
    file = models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name='图片文件')
    name = models.CharField(max_length=255, blank=True, verbose_name='名称')
    width = models.IntegerField(null=True, blank=True, verbose_name='宽度')
    height = models.IntegerField(null=True, blank=True, verbose_name='高度')
    file_size = models.IntegerField(default=0, verbose_name='文件大小')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'image_assets'
        ordering = ['-created_at']
        verbose_name = '图片素材'
        verbose_name_plural = '图片素材'

    def __str__(self):
        return self.name or f'图片-{self.id}'


class SpeechScript(models.Model):
    """演讲稿"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='speeches', verbose_name='会话')
    page = models.ForeignKey(SessionPage, on_delete=models.CASCADE, related_name='speeches', null=True, blank=True, verbose_name='关联页面')

    STYLE_CHOICES = [
        ('formal', '正式演讲'),
        ('casual', '轻松对话'),
        ('narrative', '叙事风格'),
        ('custom', '自定义'),
    ]
    style = models.CharField(max_length=10, choices=STYLE_CHOICES, default='formal', verbose_name='风格')

    content = models.TextField(verbose_name='演讲稿内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'speech_scripts'
        ordering = ['-created_at']
        verbose_name = '演讲稿'
        verbose_name_plural = '演讲稿'

    def __str__(self):
        return f'{self.session.title} - {self.get_style_display()}'
