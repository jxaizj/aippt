from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PageEdit, ElementAnimation
from sessions.models import SessionPage, SessionOperation
from django.utils import timezone


@api_view(['POST'])
def update_page_content(request):
    page_id = request.data.get('page_id')
    html_content = request.data.get('html_content', '')
    page = SessionPage.objects.get(id=page_id)
    page.html_content = html_content
    page.status = 'completed'
    page.save()
    return Response({'status': 'ok', 'page_id': str(page.id)})


@api_view(['POST'])
def move_element(request):
    page_id = request.data.get('page_id')
    selector = request.data.get('selector')
    left = request.data.get('left')
    top = request.data.get('top')
    PageEdit.objects.create(
        page_id=page_id,
        operation_id=request.data.get('operation_id'),
        element_selector=selector,
        action='move',
        after_state={'left': left, 'top': top},
    )
    return Response({'status': 'ok'})


@api_view(['POST'])
def resize_element(request):
    page_id = request.data.get('page_id')
    selector = request.data.get('selector')
    width = request.data.get('width')
    height = request.data.get('height')
    PageEdit.objects.create(
        page_id=page_id,
        operation_id=request.data.get('operation_id'),
        element_selector=selector,
        action='resize',
        after_state={'width': width, 'height': height},
    )
    return Response({'status': 'ok'})


@api_view(['POST'])
def delete_element(request):
    page_id = request.data.get('page_id')
    selector = request.data.get('selector')
    PageEdit.objects.create(
        page_id=page_id,
        operation_id=request.data.get('operation_id'),
        element_selector=selector,
        action='remove',
    )
    return Response({'status': 'ok'})


@api_view(['POST'])
def copy_element(request):
    page_id = request.data.get('page_id')
    selector = request.data.get('selector')
    PageEdit.objects.create(
        page_id=page_id,
        operation_id=request.data.get('operation_id'),
        element_selector=selector,
        action='copy',
    )
    return Response({'status': 'ok'})


@api_view(['POST'])
def add_element(request):
    page_id = request.data.get('page_id')
    element_type = request.data.get('element_type')
    element_data = request.data.get('element_data', {})
    PageEdit.objects.create(
        page_id=page_id,
        operation_id=request.data.get('operation_id'),
        action='add',
        after_state={'type': element_type, **element_data},
    )
    return Response({'status': 'ok'})


@api_view(['POST'])
def set_element_animation(request):
    page_id = request.data.get('page_id')
    selector = request.data.get('selector')
    animation_data = request.data.get('animation', {})
    anim, created = ElementAnimation.objects.update_or_create(
        page_id=page_id,
        element_selector=selector,
        defaults={
            'animation_type': animation_data.get('type', 'entrance'),
            'effect': animation_data.get('effect', 'fadeIn'),
            'trigger': animation_data.get('trigger', 'auto'),
            'duration': animation_data.get('duration', 600),
            'delay': animation_data.get('delay', 0),
            'order': animation_data.get('order', 0),
        }
    )
    return Response({'status': 'ok', 'animation_id': str(anim.id), 'created': created})


@api_view(['POST'])
def remove_element_animation(request):
    page_id = request.data.get('page_id')
    selector = request.data.get('selector')
    ElementAnimation.objects.filter(page_id=page_id, element_selector=selector).delete()
    return Response({'status': 'ok'})


@api_view(['POST'])
def reorder_pages(request):
    session_id = request.data.get('session_id')
    page_order = request.data.get('page_order', [])
    for i, page_id in enumerate(page_order):
        SessionPage.objects.filter(id=page_id).update(page_number=i + 1)
    return Response({'status': 'ok'})


@api_view(['POST'])
def delete_page(request):
    page_id = request.data.get('page_id')
    page = SessionPage.objects.get(id=page_id)
    page.deleted_at = timezone.now()
    page.save()
    return Response({'status': 'ok'})


@api_view(['POST'])
def add_page(request):
    from sessions.models import Session, SessionPage
    session_id = request.data.get('session_id')
    after_page_number = request.data.get('after_page_number', 0)
    session = Session.objects.get(id=session_id)
    pages = SessionPage.objects.filter(
        session=session, deleted_at__isnull=True,
        page_number__gt=after_page_number
    ).order_by('-page_number')
    for page in pages:
        page.page_number += 1
        page.save()
    new_page = SessionPage.objects.create(
        session=session,
        file_slug=f'page-{after_page_number + 1}',
        page_number=after_page_number + 1,
        title=f'第{after_page_number + 1}页',
        html_path=f'/sessions/{session.id}/pages/page-{after_page_number + 1}.html',
        status='pending'
    )
    return Response({'status': 'ok', 'page_id': str(new_page.id)})


@api_view(['POST'])
def undo_operation(request):
    session_id = request.data.get('session_id')
    operation = SessionOperation.objects.filter(
        session_id=session_id, status='completed'
    ).order_by('-created_at').first()
    if operation and operation.before_commit:
        operation.type = 'rollback'
        operation.save()
        return Response({'status': 'ok', 'rolled_back': str(operation.id)})
    return Response({'error': '没有可撤销的操作'}, status=400)


@api_view(['POST'])
def redo_operation(request):
    return Response({'status': 'ok'})


@api_view(['POST'])
def rollback_to_version(request):
    session_id = request.data.get('session_id')
    operation_id = request.data.get('operation_id')
    target_operation = SessionOperation.objects.get(id=operation_id)
    rollback_op = SessionOperation.objects.create(
        session_id=session_id,
        type='rollback',
        scope='session',
        target_operation=target_operation,
        target_commit=target_operation.before_commit,
        status='completed',
        completed_at=timezone.now(),
    )
    return Response({'status': 'ok', 'rollback_operation_id': str(rollback_op.id)})
