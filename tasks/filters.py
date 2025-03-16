import django_filters
from django import forms
from .models import Task, Category, Tag

class TaskFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    due_date_range = django_filters.DateTimeFromToRangeFilter(
        field_name='due_date',
        widget=django_filters.widgets.RangeWidget(attrs={'class': 'form-control', 'type': 'date'})
    )
    status = django_filters.ChoiceFilter(
        choices=Task.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    priority = django_filters.ChoiceFilter(
        choices=Task.PRIORITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Task
        fields = ['title', 'category', 'tags', 'status', 'priority', 'due_date_range']