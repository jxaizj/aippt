# AI Engine tasks - async generation tasks
from .utils import get_openai_client, safe_json_parse, get_active_provider


def generate_ppt_task(session_id, run_id, conversation_id, topic, page_count, style_id, detail, model_config=None, progress_callback=None):
    """AI生成PPT任务。progress_callback(event_dict) 用于实时推送进度。"""
    from sessions.models import Session, SessionPage, GenerationRun, GenerationPage, SessionOperation, Message, Style
    from .models import AIConversation
    from .utils import get_openai_client

    # 推送进度的便捷函数
    def notify(event):
        if progress_callback:
            try:
                progress_callback(event)
            except Exception:
                pass

    # 流式日志：持久化到 run.metadata['stream_log']，供前端轮询实时展示生成过程
    _run_ref = {'run': None}

    def log(text, append=False):
        """记录一条生成过程日志。append=True 时追加到最后一行，用于逐块流式输出。"""
        run = _run_ref.get('run')
        if not run:
            return
        try:
            meta = run.metadata or {}
            lines = meta.get('stream_log', [])
            if append and lines:
                lines[-1] = lines[-1] + text
            else:
                lines.append(text)
            meta['stream_log'] = lines
            run.metadata = meta
            run.save(update_fields=['metadata', 'updated_at'])
        except Exception:
            pass

    try:
        session = Session.objects.get(id=session_id)
        run = GenerationRun.objects.get(id=run_id)
        _run_ref['run'] = run
        conversation = AIConversation.objects.get(id=conversation_id)

        # 未指定配置时回退到激活配置
        if model_config is None:
            from sessions.models import ModelConfig
            model_config = ModelConfig.objects.filter(active=True).first()

        if not model_config or not model_config.api_key:
            run.status = 'failed'
            run.error = '未配置AI模型'
            run.save()
            log('❌ 未配置AI模型')
            notify({'type': 'generation_error', 'error': run.error})
            return

        client = get_openai_client(model_config)
        model_name = model_config.model or 'gpt-4'

        log(f'🚀 开始生成演示稿：{topic}（共 {page_count} 页）')
        log(f'🧠 使用模型：{model_name}')
        log('📋 正在规划大纲...')
        notify({'type': 'generation_status', 'message': '正在规划大纲...', 'status': 'running'})

        # 获取风格信息
        style_info = ""
        style_obj = None
        if style_id:
            style_obj = Style.objects.filter(id=style_id).first()
        elif session.style:
            style_obj = session.style

        if style_obj:
            style_parts = [f"风格名称：{style_obj.style_name}"]
            if style_obj.description:
                style_parts.append(f"风格描述：{style_obj.description}")
            if style_obj.style_skill:
                style_parts.append(f"风格指南：{style_obj.style_skill}")
            style_info = "\n".join(style_parts)
            log(f'🎨 使用风格：{style_obj.style_name}')

        # 第一步：生成大纲
        outline_system_prompt = '你是一个专业的PPT设计师，擅长创建结构清晰的演示大纲。只返回JSON格式。'
        if style_info:
            outline_system_prompt += f'\n\n当前使用的视觉风格要求：\n{style_info}'

        outline_prompt = f"""请为以下主题生成一份详细的PPT大纲，共{page_count}页。
主题：{topic}
补充说明：{detail}
{f"视觉风格：{style_obj.style_name}" if style_obj else ""}

请以JSON数组格式返回，每页包含title(标题)、content(内容描述)、layout(布局建议)。"""

        outline_response = client.chat.completions.create(
            model=model_name,
            messages=[
                {'role': 'system', 'content': outline_system_prompt},
                {'role': 'user', 'content': outline_prompt}
            ],
            temperature=0.7,
        )

        outline_content = outline_response.choices[0].message.content
        outline = safe_json_parse(outline_content, r'\[.*\]', [])

        log(f'✅ 大纲规划完成，共 {len(outline)} 页：')
        for idx, pd in enumerate(outline):
            log(f'   {idx + 1}. {pd.get("title", f"第{idx + 1}页")}')

        # 更新对话
        conversation.messages.append({
            'role': 'assistant',
            'content': f'已生成大纲，共{len(outline)}页' + (f'，使用风格：{style_obj.style_name}' if style_obj else '')
        })
        conversation.save()

        # 第二步：逐页生成HTML
        for i, page_data in enumerate(outline):
            log(f'🖌️  正在生成第 {i + 1} 页：{page_data.get("title", f"第{i + 1}页")} ...')
            gen_page = GenerationPage.objects.filter(run=run, page_number=i+1).first()
            if gen_page:
                gen_page.title = page_data.get('title', f'第{i+1}页')
                gen_page.content_outline = page_data.get('content', '')
                gen_page.layout_intent = {'layout': page_data.get('layout', '')}
                gen_page.status = 'running'
                gen_page.save()

            # 生成HTML - 注入风格信息
            html_system_prompt = '你是一个HTML幻灯片设计师，使用Tailwind CSS创建美观的PPT页面。只返回完整的HTML代码。'
            if style_info:
                html_system_prompt += f'\n\n当前使用的视觉风格要求（请严格遵循）：\n{style_info}'

            html_prompt = f"""请为以下PPT页面生成完整的HTML代码（使用Tailwind CSS）。
页面标题：{page_data.get('title', '')}
页面内容：{page_data.get('content', '')}
布局建议：{page_data.get('layout', '')}
{f"视觉风格：{style_obj.style_name}" if style_obj else ""}

要求：
1. 使用Tailwind CSS
2. 页面尺寸: {session.slide_width}x{session.slide_height}
3. 生成完整的独立HTML页面
4. 严格遵循视觉风格的配色、排版和布局要求
5. 只返回HTML代码，不要解释"""

            try:
                html_response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {'role': 'system', 'content': html_system_prompt},
                        {'role': 'user', 'content': html_prompt}
                    ],
                    temperature=0.7,
                )

                html_content = html_response.choices[0].message.content
                # 提取HTML
                if '```html' in html_content:
                    html_content = html_content.split('```html')[1].split('```')[0].strip()
                elif '```' in html_content:
                    html_content = html_content.split('```')[1].split('```')[0].strip()

                # 更新页面
                session_page = SessionPage.objects.filter(session=session, page_number=i+1).first()
                if session_page:
                    session_page.html_content = html_content
                    session_page.status = 'completed'
                    session_page.save()

                if gen_page:
                    gen_page.status = 'completed'
                    gen_page.save()

                log(f'✅ 第 {i + 1} 页生成完成')
                notify({
                    'type': 'page_completed',
                    'page_number': i + 1,
                    'title': page_data.get('title', f'第{i+1}页'),
                })

            except Exception as e:
                if gen_page:
                    gen_page.status = 'failed'
                    gen_page.error = str(e)
                    gen_page.save()

                log(f'❌ 第 {i + 1} 页生成失败：{e}')
                notify({'type': 'page_error', 'page_number': i + 1, 'error': str(e)})

        # 更新运行状态
        run.status = 'completed'
        run.save()

        log(f'🎉 全部完成！共生成 {len(outline)} 页')
        notify({
            'type': 'generation_completed',
            'total_pages': len(outline),
            'message': f'生成完成，共{len(outline)}页',
        })

        # 更新操作记录
        operation = SessionOperation.objects.filter(session=session, type='generate', status='committing').first()
        if operation:
            operation.status = 'completed'
            from django.utils import timezone
            operation.completed_at = timezone.now()
            operation.save()

        # 更新对话
        conversation.status = 'completed'
        conversation.result = {'pages_generated': len(outline), 'style_used': style_obj.style_name if style_obj else None}
        conversation.save()

        # 保存AI消息
        style_msg = f'（使用风格：{style_obj.style_name}）' if style_obj else ''
        Message.objects.create(
            session=session,
            role='assistant',
            content=f'PPT生成完成！共生成{len(outline)}页。{style_msg}',
            type='text',
        )

    except Exception as e:
        run = GenerationRun.objects.get(id=run_id)
        _run_ref['run'] = run
        run.status = 'failed'
        run.error = str(e)
        run.save()
        log(f'❌ 生成失败：{e}')
        notify({'type': 'generation_error', 'error': str(e)})


def chat_edit_task(session_id, conversation_id, operation_id, message, page_id, selector):
    """异步对话编辑任务"""
    from sessions.models import Session, SessionPage, Message, SessionOperation, Style
    from .models import AIConversation
    from .utils import get_active_provider

    try:
        session = Session.objects.get(id=session_id)
        conversation = AIConversation.objects.get(id=conversation_id)
        provider = get_active_provider()

        if not provider:
            conversation.status = 'failed'
            conversation.error = '未配置AI模型'
            conversation.save()
            return

        client = get_openai_client(provider)

        # 获取风格信息
        style_info = ""
        if session.style:
            style_parts = [f"当前视觉风格：{session.style.style_name}"]
            if session.style.description:
                style_parts.append(f"风格描述：{session.style.description}")
            style_info = "\n".join(style_parts)

        # 构建上下文
        system_content = '你是一个PPT编辑助手，可以帮助用户修改PPT页面。如果需要修改页面HTML，请返回完整的HTML代码（用```html包裹）。'
        if style_info:
            system_content += f'\n\n{style_info}\n\n请在修改时保持视觉风格的一致性。'

        context_messages = [{'role': 'system', 'content': system_content}]
        if page_id:
            page = SessionPage.objects.filter(id=page_id).first()
            if page:
                context_messages.append({
                    'role': 'system',
                    'content': f'当前页面内容：{page.html_content[:2000] if page.html_content else "空页面"}'
                })

        # 获取历史消息
        history_messages = Message.objects.filter(session=session).order_by('-created_at')[:10].values('role', 'content')
        for msg in reversed(list(history_messages)):
            context_messages.append({'role': msg['role'], 'content': msg['content']})

        context_messages.append({'role': 'user', 'content': message})

        model_name = provider.model or 'gpt-4' if provider else 'gpt-4'
        response = client.chat.completions.create(
            model=model_name,
            messages=context_messages,
            temperature=0.7,
        )

        content = response.choices[0].message.content

        # 保存AI回复
        ai_msg = Message.objects.create(
            session=session,
            role='assistant',
            content=content,
            type='text',
            chat_scope='page' if page_id else 'main',
            page_id=page_id,
            selector=selector,
        )

        # 如果包含HTML代码，更新页面
        if '```html' in content and page_id:
            html_content = content.split('```html')[1].split('```')[0].strip()
            page = SessionPage.objects.filter(id=page_id).first()
            if page:
                page.html_content = html_content
                page.save()

        # 更新对话
        conversation.status = 'completed'
        conversation.messages.append({'role': 'assistant', 'content': content})
        conversation.save()

        # 更新操作记录
        operation = SessionOperation.objects.get(id=operation_id)
        operation.status = 'completed'
        from django.utils import timezone
        operation.completed_at = timezone.now()
        operation.save()

    except Exception as e:
        conversation = AIConversation.objects.get(id=conversation_id)
        conversation.status = 'failed'
        conversation.error = str(e)
        conversation.save()


def generate_speech_task(session_id, page_id, style):
    """异步生成演讲稿"""
    from sessions.models import Session, SessionPage, SpeechScript
    from .utils import get_active_provider

    try:
        session = Session.objects.get(id=session_id)
        provider = get_active_provider()

        if not provider:
            return {'error': '未配置AI模型'}

        client = get_openai_client(provider)

        style_prompts = {
            'formal': '正式演讲风格，语言严谨专业',
            'casual': '轻松对话风格，语言自然亲切',
            'narrative': '叙事风格，语言生动有故事性',
            'custom': '自定义风格',
        }

        if page_id:
            page = SessionPage.objects.filter(id=page_id).first()
            content = f'页面标题：{page.title}\n页面内容：{page.html_content[:1000] if page.html_content else ""}'
        else:
            pages = SessionPage.objects.filter(session=session, deleted_at__isnull=True)
            content = '\n'.join([f'第{p.page_number}页: {p.title}' for p in pages])

        prompt = f"""请根据以下PPT内容生成演讲稿。
风格要求：{style_prompts.get(style, '正式风格')}

PPT内容：
{content}

请生成对应的演讲稿，包含每页的讲解内容。"""

        model_name = provider.model or 'gpt-4' if provider else 'gpt-4'
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {'role': 'system', 'content': '你是一个专业的演讲撰稿人，擅长将PPT内容转化为生动的演讲稿。'},
                {'role': 'user', 'content': prompt}
            ],
            temperature=0.7,
        )

        speech_content = response.choices[0].message.content

        # 保存演讲稿
        speech = SpeechScript.objects.create(
            session=session,
            page_id=page_id,
            style=style,
            content=speech_content,
        )

        return {'speech_id': str(speech.id), 'content': speech_content}
    except Exception as e:
        return {'error': str(e)}
