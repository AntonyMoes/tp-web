'''
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.dispatch import receiver
from django.urls import reverse
from django.db.models.signals import post_save
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404


class ProfileManager(models.Manager):
    def get_bests(self, count):
        return self.get_queryset().order_by('-rating')[:count]


class Profile(AbstractUser):
    nickname = models.CharField(max_length=20)
    avatar = models.FileField(upload_to="uploads/%Y/%m/%d/")
    rating = models.IntegerField(default=0)

    objects = ProfileManager()


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )

    vote = models.SmallIntegerField(choices=VOTES)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()


class TagManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get_most_popular(self, count):
        return self.get_queryset().annotate(num_question=models.Count('questions')).order_by('-num_question')[:count]


class Tag(models.Model):
    name = models.CharField(max_length=15)
    objects = TagManager()

    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(answer_num=models.Count('answers'))

    @staticmethod
    def get_by_id(id):
        return get_object_or_404(Question, id=id)

    def get_most_hot(self):
        return self.get_queryset().order_by('-answer_num')


class QuestionTagManager(QuestionManager):
    @staticmethod
    def get_tag_by_title(tag):
        return get_object_or_404(Tag, title=tag)

    def get(self, tag):
        return self.get_queryset().filter(tags=QuestionTagManager.get_tag_by_title(tag))


class Question(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField()
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')
    datetime = models.DateTimeField(default=datetime.now)
    votes = GenericRelation(LikeDislike, related_query_name='Questions')

    objects = QuestionManager()
    by_tag = QuestionTagManager()


class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question, models.CASCADE, related_name='answers')
    author = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='author')
    datetime = models.DateTimeField(default=datetime.now)
    votes = GenericRelation(LikeDislike, related_query_name='answers')
'''

from django.db import models
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.auth.models import AbstractUser
from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum


# Напоминалка: ForeignKey в связи один ко многим указываем на связь "один"

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


class Profile(AbstractUser):
    nickname = models.CharField(max_length=20, unique=True)
    avatar_path = models.FileField(upload_to="uploads/%Y/%m/%d/")


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Dislike'),
        (LIKE, 'Like')
    )

    vote = models.SmallIntegerField(verbose_name=u"Vote", choices=VOTES)
    user = models.ForeignKey(to="Profile", verbose_name=u"Profile", on_delete=models.SET_NULL, null=True)

    content_type = models.ForeignKey(to="contenttypes.ContentType", on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)


class Question(models.Model):
    objects = ModelManagerQuestion()
    title = models.CharField(max_length=20)
    description = models.TextField(max_length=600)
    author = models.ForeignKey(to="Profile", on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    votes = GenericRelation(to="LikeDislike", related_query_name='questions')
    datetime = models.DateTimeField(default=datetime.now)

class Answer(models.Model):
    objects = ModelManagerAnswer()
    description = models.TextField(max_length=200)
    question = models.ForeignKey(to="Question", on_delete=models.SET_NULL, null=True, related_name='answers')
    author = models.ForeignKey(to="Profile", on_delete=models.SET_NULL, null=True, related_name='answers')
    votes = GenericRelation(to="LikeDislike", related_query_name='answers')
    datetime = models.DateTimeField(default=datetime.now)

