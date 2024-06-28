from django.test import TestCase

import datetime 
from django.utils import timezone

from .models import Question

from django.urls import reverse

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_field=question_text, Pub_date = time)

class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Вопросов в базе данных нет')
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_future_question(self):
        create_question('Будущий вопрос', 30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Вопросов в базе данных нет')
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        new_question = create_question('Старый вопрос', -30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Старый вопрос')
        self.assertQuerySetEqual(response.context['latest_question_list'], [new_question])

    def test_future_question_and_past_question(self):
        create_question('Будущий вопрос', 30)
        new_question = create_question('Старый вопрос', -30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Старый вопрос')
        self.assertNotContains(response, 'Будущий вопрос')
        self.assertQuerySetEqual(response.context['latest_question_list'], [new_question])

    def test_two_past_questions(self):
        new_question = create_question('Старый вопрос', -30)
        new_question_2 = create_question('Ещё один вопрос', -5)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Старый вопрос')
        self.assertContains(response, 'Ещё один вопрос')
        self.assertQuerySetEqual(response.context['latest_question_list'], [new_question_2, new_question])

class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        future_question = create_question('Будущий вопрос', 30)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        new_question = create_question('Старый вопрос', -30)
        url = reverse('polls:detail', args=(new_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Старый вопрос')

class QuestionResultsViewTests(TestCase):

    def test_future_question(self):
        future_question = create_question('Будущий вопрос', 30)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        new_question = create_question('Старый вопрос', -30)
        url = reverse('polls:results', args=(new_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

class QuestionModelTests(TestCase):

    def test_Was_published_recently_With_Old_question(self):
        time = timezone.now() - datetime.timedelta( days=1, seconds=1)
        old_question = Question(Pub_date=time)
        self.assertIs(
            old_question.was_published_recently(), False)
    
    def test_Was_published_recently_With_Recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(Pub_date=time)
        self.assertIs(
            recent_question.was_published_recently(), True)
        
    def test_Was_published_recently_With_Future_question(self):
        time = timezone.now() + datetime.timedelta(
            days=60)
        future_question = Question(Pub_date = time)
        self.assertIs(
            future_question.was_published_recently(), False)