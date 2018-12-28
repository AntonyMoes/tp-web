from django.db import models
from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum
from .models import *


class ModelManagerQuestion(models.Manager):
    def top(self):
        return self.annotate(answer_count=Count('answers')).order_by('-answer_count')

    def get_tag(self, tag_name):
        tags = get_object_or_404(Tag, name=tag_name)
        return self.annotate(answer_count=Count('answers')).order_by().filter(tags__id=tags.id)[::-1]

    def get_list(self):
        return self.annotate(answer_count=Count('answers')).order_by()[::-1]

    def get_question(self, question_id):
        return self.annotate(answer_count=Count('answers')).get(id=question_id)


class ModelManagerAnswer(models.Manager):
    def answer(self, question_id):
        question = get_object_or_404(Question, pk=int(question_id))
        return self.filter(question__id=question.id)


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        # Забираем queryset с записями больше 0
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        # Забираем queryset с записями меньше 0
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        # Забираем суммарный рейтинг
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0