import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ask_asysoev.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from questions.models import *
from random import randint, seed, choice
from time import time
from pytils.translit import slugify

class Command(BaseCommand):
    def tag_generator(self, count):
        for _ in range(count):
          try:
            n = slugify(self.fake.text(30))
            Tag.objects.create(name= n)
          except Exception:
            pass
    
    def answer_generator(self, q, count, profiles, tags_list):
        for _ in range(count):
            user = self.fake.random_element(profiles)
            Answer.objects.create(author = user,
                                  question = q,
                                  description = self.fake.text(randint(100, 400)),
                                  datetime = self.fake.past_datetime())
    
    def question_generator(self, count, profiles, tags_list):
        for _ in range(count):
            answer_count = randint(1, 20)
            profile = self.fake.random_element(profiles)
            new_tags = self.fake.random_sample(tags_list, length=randint(1, 5))
            q = Question(title = self.fake.text(randint(50, 150)),
                         description = self.fake.text(randint(100, 400)),
                         author = profile,
                         datetime = self.fake.past_datetime())
            q.save()

            for tag in new_tags:
                q.tags.add(tag)
            q.save()
            self.answer_generator(q, answer_count, profiles, tags_list)
            
    def user_generator(self, count):
      for i in range(count):
        try:
          profile = Profile(
            username = slugify(self.fake.text(100)),
            nickname = self.fake.text(randint(3, 40)),
            email = self.fake.email())
          profile.save()

        except Exception:
          pass

    '''def marks_generator(self, count, profiles):
      answers = list(Answer.objects.all()[0:])
      questions = list(Question.objects.all()[0:])
      questions_marks = []
      answer_marks = []
 
      for i in range(count / 2):
        print(i)
        profile = profiles[randint(0, 9561)]
        answer = answers[randint(0, 866747)]
        amark = AnswerMark(post = answer, author = profile, mark_type =choice([False, True]))
        answer_marks.append(amark)
        amark.save()

        
        question = questions[randint(0, 82573)]
        qmark = QuestionMark(post = question, author = profile, mark_type = choice([False, True]))
        qmark.save()
        questions_marks.append(qmark)
      print("Saving to db ...")
      AnswerMark.objects.bulk_create(answer_marks)
      print("Saved answers...")
      QuestionMark.objects.bulk_create(questions_marks)
      counter = 0
      for q in questions:
        counter+= 1
        print(counter)
        q.rating = randint(-20000000, 20000000)
        q.save()
      counter = 0
      for a in answers:
        counter+= 1
        print(counter)
        a.rating = randint(-20000000, 20000000)
        a.save() '''

    def handle(self, *args, **options):
        self.fake = Faker()
        self.tag_generator(10000)
        self.user_generator(10000)
        profiles = list(Profile.objects.all()[0:])
        tags_list = list(Tag.objects.all()[0:])
        self.question_generator(100000, profiles, tags_list)
        #2000000
        #self.marks_generator(2000000, profiles)