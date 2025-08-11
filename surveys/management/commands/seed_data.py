"""Seed database with demo survey and questions."""
from __future__ import annotations
from datetime import date
from django.core.management.base import BaseCommand
from surveys.models import Survey, Question, Option


class Command(BaseCommand):
    help = 'Create demo survey with questions.'

    def handle(self, *args, **options):
        if Survey.objects.exists():
            self.stdout.write('Data already exists.')
            return
        survey = Survey.objects.create(
            title='Demo enquête', description='Demo data', start_date=date.today(), end_date=date.today(), is_published=True
        )
        for i in range(1, 4):
            Question.objects.create(survey=survey, number=i, title=f'Open vraag {i}', text='Uw antwoord?', question_type=Question.OPEN)
        for i in range(4, 8):
            q = Question.objects.create(survey=survey, number=i, title=f'Meerkeuze {i}', text='Kies een optie', question_type=Question.MULTIPLE_CHOICE)
            Option.objects.create(question=q, text='Optie A')
            Option.objects.create(question=q, text='Optie B')
        for i in range(8, 11):
            Question.objects.create(survey=survey, number=i, title=f'Schaal {i}', text='Geef een waarde', question_type=Question.SCALE)
        self.stdout.write('Demo data aangemaakt.')
