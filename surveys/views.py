"""Views for survey management and participation."""
from __future__ import annotations
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.http import StreamingHttpResponse
import csv

from .forms import SurveyForm, QuestionForm, DynamicResponseForm
from .models import Survey, Question, Option, Invitation, Answer


class SurveyListView(LoginRequiredMixin, ListView):
    model = Survey
    template_name = 'surveys/survey_list.html'


class SurveyCreateView(LoginRequiredMixin, CreateView):
    model = Survey
    form_class = SurveyForm
    template_name = 'surveys/survey_form.html'
    success_url = reverse_lazy('survey_list')


class SurveyUpdateView(LoginRequiredMixin, UpdateView):
    model = Survey
    form_class = SurveyForm
    template_name = 'surveys/survey_form.html'
    success_url = reverse_lazy('survey_list')


class SurveyDeleteView(LoginRequiredMixin, DeleteView):
    model = Survey
    template_name = 'surveys/survey_confirm_delete.html'
    success_url = reverse_lazy('survey_list')


@login_required
def question_list(request: HttpRequest, survey_id: int) -> HttpResponse:
    survey = get_object_or_404(Survey, pk=survey_id)
    questions = survey.questions.all()
    return render(request, 'surveys/question_list.html', {'survey': survey, 'questions': questions})


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'surveys/question_form.html'

    def get_initial(self):
        survey = get_object_or_404(Survey, pk=self.kwargs['survey_id'])
        return {'survey': survey}

    def get_success_url(self):
        return reverse('question_list', args=[self.object.survey.id])


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'surveys/question_form.html'

    def get_success_url(self):
        return reverse('question_list', args=[self.object.survey.id])


class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = Question
    template_name = 'surveys/question_confirm_delete.html'

    def get_success_url(self):
        return reverse('question_list', args=[self.object.survey.id])


@login_required
def create_invitation(request: HttpRequest, survey_id: int) -> HttpResponse:
    survey = get_object_or_404(Survey, pk=survey_id)
    invitation = Invitation.objects.create(survey=survey)
    link = request.build_absolute_uri(reverse('respond', args=[invitation.uuid]))
    return render(request, 'surveys/invitation_form.html', {'link': link, 'survey': survey})


@csrf_protect
def respond(request: HttpRequest, uuid_str: str) -> HttpResponse:
    invitation = get_object_or_404(Invitation, uuid=uuid_str)
    survey = invitation.survey
    questions = survey.questions.all()
    if request.method == 'POST':
        form = DynamicResponseForm(request.POST, questions=list(questions))
        if form.is_valid():
            for q in questions:
                field_value = form.cleaned_data[str(q.id)]
                if q.question_type == Question.OPEN:
                    Answer.objects.create(invitation=invitation, question=q, text=field_value)
                elif q.question_type == Question.MULTIPLE_CHOICE:
                    option = get_object_or_404(Option, pk=field_value)
                    Answer.objects.create(invitation=invitation, question=q, option=option)
                else:
                    Answer.objects.create(invitation=invitation, question=q, scale=field_value)
            invitation.responded_at = timezone.now()
            invitation.save()
            return render(request, 'surveys/thanks.html', {'survey': survey})
    else:
        form = DynamicResponseForm(questions=list(questions))
    return render(request, 'surveys/response_form.html', {'form': form, 'survey': survey})


@login_required
def results(request: HttpRequest, survey_id: int) -> HttpResponse:
    survey = get_object_or_404(Survey, pk=survey_id)
    answers = Answer.objects.filter(invitation__survey=survey).select_related('question', 'option')
    return render(request, 'surveys/results.html', {'survey': survey, 'answers': answers})


@login_required
def results_csv(request: HttpRequest, survey_id: int) -> HttpResponse:
    survey = get_object_or_404(Survey, pk=survey_id)

    def generate():
        yield 'question,answer,timestamp\n'
        for ans in Answer.objects.filter(invitation__survey=survey):
            if ans.question.question_type == Question.OPEN:
                value = ans.text
            elif ans.question.question_type == Question.MULTIPLE_CHOICE:
                value = ans.option.text if ans.option else ''
            else:
                value = str(ans.scale)
            yield f'"{ans.question.title}","{value}",{ans.created_at.isoformat()}\n'

    response = StreamingHttpResponse(generate(), content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="survey_{survey_id}_results.csv"'
    return response
