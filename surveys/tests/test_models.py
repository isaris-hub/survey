"""Tests for survey models."""
from datetime import date
from django.core.exceptions import ValidationError
from django.test import TestCase
from surveys.models import Survey, Question


class SurveyModelTests(TestCase):
    def test_end_date_not_before_start(self) -> None:
        survey = Survey(title='t', description='d', start_date=date(2024, 1, 2), end_date=date(2024, 1, 1))
        with self.assertRaises(ValidationError):
            survey.clean()

    def test_publish_requires_min_questions(self) -> None:
        survey = Survey.objects.create(title='t', description='d', start_date=date.today(), end_date=date.today(), is_published=True)
        with self.assertRaises(ValidationError):
            survey.clean()
        for i in range(10):
            Question.objects.create(survey=survey, number=i+1, title=f'q{i}', text='t', question_type=Question.OPEN)
        survey.clean()  # should not raise
