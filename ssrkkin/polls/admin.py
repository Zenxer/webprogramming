from django.contrib import admin

from .models import Question, Choice

class ChoiceAdmin(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_field", "Pub_date", "was_published_recently"]
    fieldsets = [
        (None, {"fields": ["question_field"]}),
        ("Data information", {"fields": ["Pub_date"]})
    ]
    inlines = [ChoiceAdmin]
    search_fields = ["question_field"]

admin.site.register(Question, QuestionAdmin)
