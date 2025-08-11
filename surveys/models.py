"""Database models for surveys."""
from __future__ import annotations
import uuid
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models


class Survey(models.Model):
    """Survey definition."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_published = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Enquête'
        verbose_name_plural = 'Enquêtes'

    def __str__(self) -> str:
        return self.title

    def clean(self) -> None:
        if self.end_date < self.start_date:
            raise ValidationError('Einddatum moet groter of gelijk zijn aan startdatum.')
        if self.is_published and self.questions.count() < 10:
            raise ValidationError('Enquête moet minimaal 10 vragen hebben voor publicatie.')


class Question(models.Model):
    """Question belonging to a survey."""
    OPEN = 'open'
    MULTIPLE_CHOICE = 'mc'
    SCALE = 'scale'
    QUESTION_TYPES = [
        (OPEN, 'Open'),
        (MULTIPLE_CHOICE, 'Meerkeuze'),
        (SCALE, 'Schaal'),
    ]

    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    text = models.TextField()
    image_url = models.URLField(blank=True)
    table_description = models.CharField(max_length=200, blank=True)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)

    class Meta:
        ordering = ['number']

    def __str__(self) -> str:
        return f"{self.number}. {self.title}"


class Option(models.Model):
    """Option for multiple-choice question."""
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.text


class Invitation(models.Model):
    """Unique link for survey participation."""
    survey = models.ForeignKey(Survey, related_name='invitations', on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return str(self.uuid)


class Answer(models.Model):
    """Answer given by a respondent."""
    invitation = models.ForeignKey(Invitation, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=2000, blank=True)
    option = models.ForeignKey(Option, null=True, blank=True, on_delete=models.SET_NULL)
    scale = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self) -> None:
        qt = self.question.question_type
        if qt == Question.OPEN and not self.text:
            raise ValidationError('Tekstantwoord is vereist.')
        if qt == Question.MULTIPLE_CHOICE and not self.option:
            raise ValidationError('Kies één optie.')
        if qt == Question.SCALE:
            if self.scale is None:
                raise ValidationError('Schaalwaarde vereist.')
            if self.scale < Decimal('0') or self.scale > Decimal('1'):
                raise ValidationError('Schaalwaarde tussen 0 en 1.')

    def __str__(self) -> str:
        return f"{self.question}"
