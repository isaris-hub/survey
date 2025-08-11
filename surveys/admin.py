"""Admin registrations for surveys."""
from django.contrib import admin
from .models import Survey, Question, Option, Invitation, Answer


class OptionInline(admin.TabularInline):
    model = Option
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
    list_display = ('survey', 'number', 'title', 'question_type')
    list_filter = ('survey',)


admin.site.register(Survey)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Invitation)
admin.site.register(Answer)
