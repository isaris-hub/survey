"""URL configuration for surveys app."""
from django.urls import path
from . import views

urlpatterns = [
    path('survey/add/', views.SurveyCreateView.as_view(), name='survey_add'),
    path('survey/<int:pk>/edit/', views.SurveyUpdateView.as_view(), name='survey_edit'),
    path('survey/<int:pk>/delete/', views.SurveyDeleteView.as_view(), name='survey_delete'),
    path('survey/<int:survey_id>/questions/', views.question_list, name='question_list'),
    path('survey/<int:survey_id>/questions/add/', views.QuestionCreateView.as_view(), name='question_add'),
    path('question/<int:pk>/edit/', views.QuestionUpdateView.as_view(), name='question_edit'),
    path('question/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
    path('survey/<int:survey_id>/invite/', views.create_invitation, name='invite'),
    path('respond/<uuid_str>/', views.respond, name='respond'),
    path('survey/<int:survey_id>/results/', views.results, name='results'),
    path('survey/<int:survey_id>/results/csv/', views.results_csv, name='results_csv'),
]
