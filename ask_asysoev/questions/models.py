from django.db import models
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.auth.models import AbstractUser
from .managers import LikeDislikeManager, ModelManagerQuestion, ModelManagerAnswer


# Напоминалка: ForeignKey в связи один ко многим указываем на связь "один"


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
    question = models.ForeignKey(to="Question", on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(to="Profile", on_delete=models.SET_NULL, null=True, related_name='answers')
    votes = GenericRelation(to="LikeDislike", related_query_name='answers')
    datetime = models.DateTimeField(default=datetime.now)

