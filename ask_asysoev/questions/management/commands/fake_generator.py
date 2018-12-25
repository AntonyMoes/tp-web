from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from faker import Faker
from questions.models import *
from random import randint, seed, choice
from time import time


class Command(BaseCommand):

    def tag_generator(self, count):
        for _ in range(count):
            try:
                Tag.objects.create(name=self.fake.text(10).split()[0].rstrip('.'))
            except:
                print('Tagerror')

    def user_generator(self, count):
        for _ in range(count):
            try:
                Profile.objects.create(username=self.fake.user_name(),
                                       nickname=self.fake.user_name(),
                                       password=self.fake.password(20),
                                       email=self.fake.email())
            except:
                print('Usererror')

    def answer_generator(self, q, count, profiles, tags_list):
        for _ in range(count):
            auth = self.fake.random_element(profiles)
            Answer.objects.create(text=self.fake.text(100),
                                  author=auth,
                                  question=q)

    def question_generator(self, count, profiles, tags_list):
        q = None
        for _ in range(count):
            try:
                profile = self.fake.random_element(profiles)
                new_tags = self.fake.random_sample(tags_list, length=randint(1, 3))
                q = Question(title=self.fake.text(20),
                             text=self.fake.text(100),
                             author=profile)
                q.save()
                for tag in new_tags:
                    q.tags.add(tag)
                q.save()
            except:
                print('Questionerror')
            self.answer_generator(q, randint(1, 5), profiles, tags_list)

    def votes_questions_generator(self, count, profiles, questions, answers):
        for _ in range(count):
            profile = self.fake.random_element(profiles)
            question = self.fake.random_element(questions)
            answer = self.fake.random_element(answers)

            q_model_type = ContentType.objects.get_for_model(question)
            LikeDislike.objects.create(content_type=q_model_type,
                                       object_id=question.id,
                                       user=profile,
                                       vote=choice((1, -1)))

            a_model_type = ContentType.objects.get_for_model(answer)
            LikeDislike.objects.create(content_type=a_model_type,
                                       object_id=answer.id,
                                       user=profile,
                                       vote=choice((1, -1)))

    def handle(self, *args, **options):
        self.fake = Faker()
        profiles = list(Profile.objects.all()[1:])
        tags_list = list(Tag.objects.all()[0:])
        questions = list(Question.objects.all()[0:])
        answers = list(Answer.objects.all()[0:])
        self.tag_generator(10)
        self.user_generator(4)
        self.question_generator(10, profiles, tags_list)
        self.votes_questions_generator(10, profiles, questions, answers)
