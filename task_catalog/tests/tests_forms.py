from django.contrib.auth import get_user_model
from django.test import TestCase

from task_catalog.forms import TaskForm, SignUpForm, WorkerUpdateForm
from task_catalog.models import TaskType, Position


class FormValidationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.task_type = TaskType.objects.create(name='Feature')
        self.position = Position.objects.create(name='Tester')

    def test_task_form_valid(self):
        form_data = {
            'name': 'New Task',
            'description': 'Task description',
            'deadline': '2025-12-31',
            'priority': 'High',
            'task_type': self.task_type.id,
            'workers': [self.user.id]
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_form_missing_deadline(self):
        form_data = {
            'name': 'Task without deadline',
            'description': 'No deadline',
            'priority': 'High',
            'task_type': self.task_type.id,
            'workers': [self.user.id]
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('deadline', form.errors)

    def test_task_form_optional_task_type(self):
        form_data = {
            'name': 'Task with no type',
            'description': 'Testing optional type',
            'deadline': '2025-12-31',
            'priority': 'Low',
            'workers': [self.user.id]
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_signup_form_email_required(self):
        form_data = {
            'username': 'signupuser',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_worker_update_form_with_position(self):
        form_data = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'position': self.position.id
        }
        form = WorkerUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_worker_update_form_without_position(self):
        form_data = {
            'username': 'testuser',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane@example.com'
        }
        form = WorkerUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())