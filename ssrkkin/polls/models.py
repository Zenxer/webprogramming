from django.db import models

import datetime
from django.utils import timezone
from django.contrib import admin

class Question(models.Model):
    question_field = models.CharField(max_length = 200)
    Pub_date = models.DateTimeField("date published")
    @admin.display(
            boolean = True,
            description = "Опубликован недавно?"
    )
    def was_published_recently(self):

        return timezone.now() >= self.Pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)