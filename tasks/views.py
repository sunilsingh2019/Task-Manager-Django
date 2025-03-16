from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from django.utils import timezone
from django.db.models import Q, Count, Sum
from django.http import HttpResponse, JsonResponse
import json
from .models import (
    Task, Comment, Category, Tag, ActivityLog,
    TaskTemplate, TaskAttachment, TimeEntry
)
from .forms import (
    TaskForm, UserRegistrationForm, CommentForm,
    CategoryForm, TagForm, TaskTemplateForm,
    TaskAttachmentForm, TimeEntryForm
)
from .filters import TaskFilter

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('task_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    total_tasks = Task.objects.filter(assigned_to=request.user).count()
    completed_tasks = Task.objects.filter(assigned_to=request.user, status='done').count()
    pending_tasks = Task.objects.filter(assigned_to=request.user).exclude(status='done').count()
    overdue_tasks = Task.objects.filter(
        assigned_to=request.user,
        due_date__lt=timezone.now()
    ).exclude(status='done').count()
    recent_activities = ActivityLog.objects.filter(
        Q(task__assigned_to=request.user) | Q(task__created_by=request.user)
    )[:10]
    
    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,
        'recent_activities': recent_activities,
        'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    }
    return render(request, 'tasks/dashboard.html', context)

@login_required
def task_list(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    task_filter = TaskFilter(request.GET, queryset=tasks)
    
    # Get task statistics by category
    category_stats = Category.objects.filter(tasks__assigned_to=request.user).annotate(
        task_count=Count('tasks')
    )
    
    context = {
        'filter': task_filter,
        'tasks': task_filter.qs,
        'category_stats': category_stats
    }
    return render(request, 'tasks/task_list.html', context)

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    comments = task.comments.all()
    activities = task.activities.all()
    dependencies = task.dependencies.all()
    dependent_tasks = task.dependent_tasks.all()
    attachments = task.attachments.all()
    time_entries = task.time_entries.all()
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            
            # Log the comment activity
            ActivityLog.objects.create(
                task=task,
                user=request.user,
                action='comment',
                description=f'Commented: {comment.content[:50]}...'
            )
            
            messages.success(request, 'Comment added successfully!')
            return redirect('task_detail', pk=pk)
    else:
        comment_form = CommentForm()
    
    context = {
        'task': task,
        'comments': comments,
        'activities': activities,
        'dependencies': dependencies,
        'dependent_tasks': dependent_tasks,
        'comment_form': comment_form,
        'attachments': attachments,
        'time_entries': time_entries,
    }
    return render(request, 'tasks/task_detail.html', context)

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            form.save_m2m()  # Save many-to-many relationships
            
            # Log the creation activity
            ActivityLog.objects.create(
                task=task,
                user=request.user,
                action='create',
                description=f'Created task: {task.title}'
            )
            
            messages.success(request, 'Task created successfully!')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(user=request.user)
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Create Task'})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            task = form.save()
            
            # Log the update activity
            ActivityLog.objects.create(
                task=task,
                user=request.user,
                action='update',
                description=f'Updated task: {task.title}'
            )
            
            messages.success(request, 'Task updated successfully!')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task, user=request.user)
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Update Task'})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.created_by = request.user
            category.save()
            messages.success(request, 'Category created successfully!')
            return redirect('task_list')
    else:
        form = CategoryForm()
    return render(request, 'tasks/category_form.html', {'form': form})

@login_required
def tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.created_by = request.user
            tag.save()
            messages.success(request, 'Tag created successfully!')
            return redirect('task_list')
    else:
        form = TagForm()
    return render(request, 'tasks/tag_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def template_list(request):
    templates = TaskTemplate.objects.filter(created_by=request.user)
    return render(request, 'tasks/template_list.html', {'templates': templates})

@login_required
def template_create(request):
    if request.method == 'POST':
        form = TaskTemplateForm(request.POST)
        if form.is_valid():
            template = form.save(commit=False)
            template.created_by = request.user
            template.save()
            messages.success(request, 'Template created successfully!')
            return redirect('template_list')
    else:
        form = TaskTemplateForm()
    return render(request, 'tasks/template_form.html', {'form': form, 'title': 'Create Template'})

@login_required
def task_from_template(request, template_id):
    template = get_object_or_404(TaskTemplate, pk=template_id, created_by=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.template = template
            task.save()
            form.save_m2m()
            messages.success(request, 'Task created from template successfully!')
            return redirect('task_detail', pk=task.pk)
    else:
        initial = {
            'description': template.description,
            'category': template.category,
            'priority': template.priority,
            'estimated_time': template.estimated_time,
        }
        form = TaskForm(user=request.user, initial=initial)
    return render(request, 'tasks/task_form.html', {
        'form': form,
        'title': f'Create Task from Template: {template.name}'
    })

@login_required
def attachment_upload(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskAttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.task = task
            attachment.uploaded_by = request.user
            attachment.save()
            
            # Log the attachment activity
            ActivityLog.objects.create(
                task=task,
                user=request.user,
                action='update',
                description=f'Added attachment: {attachment.filename()}'
            )
            
            messages.success(request, 'File uploaded successfully!')
            return redirect('task_detail', pk=task_id)
    else:
        form = TaskAttachmentForm()
    
    return render(request, 'tasks/attachment_form.html', {
        'form': form,
        'task': task
    })

@login_required
def time_entry_create(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TimeEntryForm(request.POST)
        if form.is_valid():
            time_entry = form.save(commit=False)
            time_entry.task = task
            time_entry.user = request.user
            time_entry.save()
            
            # Update task's actual time
            task.update_actual_time()
            
            messages.success(request, 'Time entry added successfully!')
            return redirect('task_detail', pk=task_id)
    else:
        form = TimeEntryForm()
    
    return render(request, 'tasks/time_entry_form.html', {
        'form': form,
        'task': task
    })

@login_required
def task_statistics(request):
    # Task statistics by status
    status_stats = Task.objects.filter(
        assigned_to=request.user
    ).values('status').annotate(count=Count('id'))
    
    # Time spent on tasks
    time_spent = TimeEntry.objects.filter(
        task__assigned_to=request.user
    ).aggregate(total_time=Sum('duration'))
    
    # Tasks by priority
    priority_stats = Task.objects.filter(
        assigned_to=request.user
    ).values('priority').annotate(count=Count('id'))
    
    # Overdue tasks
    overdue_count = Task.objects.filter(
        assigned_to=request.user,
        due_date__lt=timezone.now(),
        status__in=['todo', 'in_progress']
    ).count()
    
    context = {
        'status_stats': status_stats,
        'time_spent': time_spent['total_time'],
        'priority_stats': priority_stats,
        'overdue_count': overdue_count
    }
    return render(request, 'tasks/statistics.html', context)

@login_required
def kanban_board(request):
    tasks_todo = Task.objects.filter(assigned_to=request.user, status='todo')
    tasks_in_progress = Task.objects.filter(assigned_to=request.user, status='in_progress')
    tasks_done = Task.objects.filter(assigned_to=request.user, status='done')
    
    context = {
        'tasks_todo': tasks_todo,
        'tasks_in_progress': tasks_in_progress,
        'tasks_done': tasks_done,
    }
    return render(request, 'tasks/kanban.html', context)

@login_required
def update_task_status(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id, assigned_to=request.user)
        data = json.loads(request.body)
        new_status = data.get('status')
        
        if new_status in dict(Task.STATUS_CHOICES):
            old_status = task.status
            task.status = new_status
            if new_status == 'done':
                task.mark_completed()
            task.save()
            
            # Log the status change
            ActivityLog.objects.create(
                task=task,
                user=request.user,
                action='status',
                description=f'Changed status from {old_status} to {new_status}'
            )
            
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
