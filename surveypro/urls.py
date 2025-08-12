"""Main URL configuration for SurveyPro."""
from django.contrib import admin
from django.urls import include, path
from surveys import views as survey_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', survey_views.home, name='home'),
    path('surveys/', survey_views.SurveyListView.as_view(), name='survey_list'),
    path('', include('surveys.urls')),
]
