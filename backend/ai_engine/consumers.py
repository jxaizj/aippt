import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class GenerationConsumer(AsyncWebsocketConsumer):
    """WebSocket消费者 - AI生成进度实时推送"""

    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.room_group_name = f'generation_{self.session_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'start_generation':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'generation_status',
                    'message': '开始生成...',
                    'status': 'running',
                    'progress': 0,
                }
            )
        elif action == 'cancel_generation':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'generation_status',
                    'message': '已取消',
                    'status': 'cancelled',
                    'progress': 0,
                }
            )

    async def generation_status(self, event):
        await self.send(text_data=json.dumps({
            'type': 'generation_status',
            'message': event['message'],
            'status': event['status'],
            'progress': event.get('progress', 0),
            'page_number': event.get('page_number'),
            'total_pages': event.get('total_pages'),
        }))

    async def page_completed(self, event):
        await self.send(text_data=json.dumps({
            'type': 'page_completed',
            'page_number': event['page_number'],
            'title': event.get('title', ''),
            'html_content': event.get('html_content', ''),
        }))

    async def generation_completed(self, event):
        await self.send(text_data=json.dumps({
            'type': 'generation_completed',
            'total_pages': event.get('total_pages', 0),
            'message': event.get('message', '生成完成'),
        }))

    async def generation_error(self, event):
        await self.send(text_data=json.dumps({
            'type': 'generation_error',
            'error': event.get('error', '未知错误'),
        }))


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket消费者 - 对话消息实时推送"""

    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.room_group_name = f'chat_{self.session_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'send_message':
            # 广播消息给房间内所有人
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': data.get('message', ''),
                    'role': 'user',
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'role': event.get('role', 'assistant'),
            'timestamp': event.get('timestamp', ''),
        }))

    async def ai_response(self, event):
        await self.send(text_data=json.dumps({
            'type': 'ai_response',
            'message': event['message'],
            'role': 'assistant',
            'streaming': event.get('streaming', False),
        }))


class NotificationConsumer(AsyncWebsocketConsumer):
    """WebSocket消费者 - 全局通知"""

    async def connect(self):
        self.room_group_name = 'notifications'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def notify(self, event):
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'title': event.get('title', ''),
            'message': event.get('message', ''),
            'level': event.get('level', 'info'),
        }))
