from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from task_catalog.models import Task, TaskType, Position


class PublicTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.task = Task.objects.create(
            name='Sample Task',
            description='desc',
            deadline=datetime.today(),
            priority='High',
            is_completed=False
        )

    def test_register_view_accessible(self):
        response = self.client.get(reverse('task_catalog:register'))
        self.assertEqual(response.status_code, 200)

    def test_profile_update_redirects(self):
        response = self.client.get(reverse('task_catalog:profile-update'))
        self.assertRedirects(response, '/accounts/login/?next=/profile/edit/')

    def test_mark_task_done_redirects(self):
        response = self.client.post(reverse('task_catalog:task-done', args=[self.task.id]))
        self.assertRedirects(response, f'/accounts/login/?next=/tasks/{self.task.id}/done/')

    def test_modal_create_task_type_redirects(self):
        response = self.client.post(reverse('task_catalog:tasktype-create'))
        self.assertRedirects(response, '/accounts/login/?next=/task-types/create/')

    def test_modal_create_position_redirects(self):
        response = self.client.post(reverse('task_catalog:position-create'))
        self.assertRedirects(response, '/accounts/login/?next=/positions/create/')


class LoggedInTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='user', password='pass')
        self.client.force_login(self.user)
        self.task_type = TaskType.objects.create(name='Bug')
        priorities = ['Low', 'Medium', 'High', 'Urgent']
        for p in priorities:
            Task.objects.create(
                name=f'Task {p}',
                description='Test task',
                deadline=datetime.today(),
                priority=p,
                is_completed=False,
                task_type=self.task_type
            )

    def test_task_board_priority_ordering(self):
        response = self.client.get(reverse('task_catalog:index'))
        tasks = list(response.context['todo_page'])
        priorities = [task.priority for task in tasks]
        self.assertEqual(priorities, ['Urgent', 'High', 'Medium'])

    def test_task_board_filter_query(self):
        response = self.client.get(reverse('task_catalog:index'), {'q': 'Urgent'})
        tasks = list(response.context['todo_page'])
        self.assertTrue(all('Urgent' in task.name for task in tasks))

    def test_register_valid(self):
        self.client.logout()
        response = self.client.post(reverse('task_catalog:register'), {
            'username': 'newuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'email': 'user@example.com'
        })
        self.assertRedirects(response, reverse('task_catalog:index'))
        self.assertTrue(get_user_model().objects.filter(username='newuser').exists())

    def test_update_profile(self):
        response = self.client.post(reverse('task_catalog:profile-update'), {
            'username': 'user',
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'new@example.com'
        })
        self.assertRedirects(response, reverse('task_catalog:workers_list'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')

    def test_mark_task_done(self):
        task = Task.objects.create(
            name='New Task',
            description='desc',
            deadline=datetime.today(),
            priority='High',
            is_completed=False
        )
        response = self.client.post(reverse('task_catalog:task-done', args=[task.id]))
        self.assertRedirects(response, reverse('task_catalog:index'))
        task.refresh_from_db()
        self.assertTrue(task.is_completed)

    def test_create_task_type(self):
        response = self.client.post(reverse('task_catalog:tasktype-create'), {
            'name': 'Design'
        }, HTTP_REFERER=f"/task/1/update/")
        self.assertRedirects(response, '/task/1/update/')
        self.assertTrue(TaskType.objects.filter(name='Design').exists())

    def test_create_position(self):
        response = self.client.post(reverse('task_catalog:position-create'), {
            'name': 'Developer'
        }, HTTP_REFERER='/profile/edit/')
        self.assertRedirects(response, '/profile/edit/')
        self.assertTrue(Position.objects.filter(name='Developer').exists())