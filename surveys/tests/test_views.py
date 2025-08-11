"""View tests for surveys."""
from datetime import date
from django.contrib.auth.models import User
from django.test import TestCase
from surveys.models import Survey


class SurveyViewTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user('admin', 'a@example.com', 'pass')

    def test_create_survey(self) -> None:
        self.client.login(username='admin', password='pass')
        response = self.client.post('/survey/add/', {
            'title': 'Test',
            'description': 'Desc',
            'is_published': False,
            'start_date': '2024-01-01',
            'end_date': '2024-01-02',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Survey.objects.count(), 1)

    def test_login_required(self) -> None:
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
