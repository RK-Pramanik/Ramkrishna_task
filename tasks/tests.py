from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from .models import Task

class TaskTest(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username='t', password='pwd', role='teacher')
        self.student = User.objects.create_user(username='s', password='pwd', role='student')

    def test_create_task(self):
        self.client.login(username='t', password='pwd')
        resp = self.client.post(reverse('tasks:create'), data={
            'title': 'Test',
            'description': 'desc',
            'assigned_to': self.student.pk,
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Task.objects.filter(title='Test').exists())
