"""Forms for surveys application."""
from __future__ import annotations
from decimal import Decimal
from typing import Any
from django import forms
from django.forms import ModelForm
from .models import Survey, Question, Option, Answer


class SurveyForm(ModelForm):
    class Meta:
        model = Survey
        fields = ['title', 'description', 'is_published', 'start_date', 'end_date']


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['survey', 'number', 'title', 'text', 'image_url', 'table_description', 'question_type']


class OptionForm(ModelForm):
    class Meta:
        model = Option
        fields = ['text']


class DynamicResponseForm(forms.Form):
    """Builds fields dynamically for questions."""
    def __init__(self, *args: Any, questions: list[Question], **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for q in questions:
            if q.question_type == Question.OPEN:
                self.fields[str(q.id)] = forms.CharField(
                    label=q.title, widget=forms.Textarea, max_length=2000
                )
            elif q.question_type == Question.MULTIPLE_CHOICE:
                choices = [(opt.id, opt.text) for opt in q.options.all()]
                self.fields[str(q.id)] = forms.ChoiceField(
                    label=q.title, choices=choices, widget=forms.RadioSelect
                )
            else:
                self.fields[str(q.id)] = forms.DecimalField(
                    label=q.title, min_value=Decimal('0'), max_value=Decimal('1'),
                    decimal_places=1, step_size=Decimal('0.1')
                )
