from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm

from task_catalog.models import Task, TaskType, Position


class TaskForm(forms.ModelForm):
    workers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'id_workers'})
    )
    deadline = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        ),
        input_formats=['%Y-%m-%d'],
    )
    task_type = forms.ModelChoiceField(
        queryset=TaskType.objects.all(),
        required=False,
        empty_label="Select a type",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_task_type'
        })
    )

    class Meta:
        model = Task
        fields = "__all__"
        exclude = ["is_completed"]


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")


class WorkerUpdateForm(forms.ModelForm):
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'position']
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),
        }


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ["name"]