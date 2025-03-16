from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/<int:pk>/update/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('categories/create/', views.category_create, name='category_create'),
    path('tags/create/', views.tag_create, name='tag_create'),
    
    # New URLs for advanced features
    path('templates/', views.template_list, name='template_list'),
    path('templates/create/', views.template_create, name='template_create'),
    path('templates/<int:template_id>/use/', views.task_from_template, name='task_from_template'),
    
    path('tasks/<int:task_id>/attachments/upload/', views.attachment_upload, name='attachment_upload'),
    path('tasks/<int:task_id>/time-entries/add/', views.time_entry_create, name='time_entry_create'),
    path('tasks/<int:task_id>/status/update/', views.update_task_status, name='update_task_status'),
    
    path('kanban/', views.kanban_board, name='kanban_board'),
    path('statistics/', views.task_statistics, name='task_statistics'),
]