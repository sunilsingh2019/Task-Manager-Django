from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_summernote.widgets import SummernoteWidget
from .models import Task, Comment, Category, Tag, TaskAttachment, TaskTemplate, TimeEntry

class TaskForm(forms.ModelForm):
    dependencies = forms.ModelMultipleChoiceField(
        queryset=Task.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'status', 
                 'assigned_to', 'category', 'tags', 'dependencies', 'template',
                 'estimated_time']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': SummernoteWidget(),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'estimated_time': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'HH:MM:SS'
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Filter dependencies to exclude current task and completed tasks
            if self.instance.pk:
                self.fields['dependencies'].queryset = Task.objects.exclude(
                    pk=self.instance.pk
                ).exclude(status='done')
            # Filter categories to show only user's categories
            self.fields['category'].queryset = Category.objects.filter(created_by=user)
            self.fields['tags'].queryset = Tag.objects.filter(created_by=user)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'})
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'color']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'})
        }

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class TaskAttachmentForm(forms.ModelForm):
    class Meta:
        model = TaskAttachment
        fields = ['file', 'description']

class TaskTemplateForm(forms.ModelForm):
    class Meta:
        model = TaskTemplate
        fields = ['name', 'description', 'category', 'priority', 'estimated_time']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'estimated_time': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'})
        }

class TimeEntryForm(forms.ModelForm):
    class Meta:
        model = TimeEntry
        fields = ['start_time', 'end_time', 'description']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 2})
        }