from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'status', 'due_date', 'assigned_to', 'created_by')
    list_filter = ('priority', 'status', 'created_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_date'
