from django.urls import path
from . import views

urlpatterns = [
    path('update-page/', views.update_page_content, name='editor-update-page'),
    path('move-element/', views.move_element, name='editor-move-element'),
    path('resize-element/', views.resize_element, name='editor-resize-element'),
    path('delete-element/', views.delete_element, name='editor-delete-element'),
    path('copy-element/', views.copy_element, name='editor-copy-element'),
    path('add-element/', views.add_element, name='editor-add-element'),
    path('set-animation/', views.set_element_animation, name='editor-set-animation'),
    path('remove-animation/', views.remove_element_animation, name='editor-remove-animation'),
    path('reorder-pages/', views.reorder_pages, name='editor-reorder-pages'),
    path('delete-page/', views.delete_page, name='editor-delete-page'),
    path('add-page/', views.add_page, name='editor-add-page'),
    path('undo/', views.undo_operation, name='editor-undo'),
    path('redo/', views.redo_operation, name='editor-redo'),
    path('rollback/', views.rollback_to_version, name='editor-rollback'),
]
