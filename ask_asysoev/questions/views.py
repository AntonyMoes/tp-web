from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage
from django.views import View
from .models import *
from .forms import *

'''
class User:
    nickname = "nick"

    def __init__(self, **kwargs):
        self.nickname = kwargs['nickname']


class Tag:
    name = "Tag"

    def __init__(self, **kwargs):
        self.name = kwargs['name']


class Comment:
    description = "Generic comment description"
    time = 3
    rating = 19


class Post(Comment):
    title = "Title"
    description = "This is just a generic description for a generic post"
    time = 3
    # for i in range(3,20):
    #     tags.append('Tag'+str(i))
    id = 123
    # pic = "a625f892fe81b6b562c3f08c163307d5_80x80.png"
    answers = 5
    rating = 19
    tags = []
    for i in range(0, 6):
        tags.append(Tag(name="Tag"+str(i)))



class IndexView(TemplateView):
    template_name = "index.html"
    extra_context = {}
    posts = []
    for i in range(0, 20):
        posts.append(Post)

    # tags = ['PostgreSQL', 'C++', 'Bootstrap', 'C', 'Python', 'Django', 'Boost']
    tags = []
    for i in range(0, 6):
        tags.append(Tag(name="Tag"+str(i)))
    # best = ['Alice', 'Savva', 'Michael', 'Vladimir', 'Nikita', 'Tony']
    best = []
    for i in range(0, 6):
        best.append(User(nickname="User"+str(i)))

    extra_context['tags'] = tags
    extra_context['best'] = best
    extra_context['posts'] = posts
    extra_context['mode'] = 'new'


class SignupView(TemplateView):
    template_name = "signup.html"
    user = 'AntonyMo'


class LoginView(TemplateView):
    template_name = "login.html"


class QuestionView(TemplateView):
    template_name = "question.html"
    extra_context = {}
    post = Post()
    comment = Comment()
    answers = []
    for i in range(0, 5):
        answers.append(comment)

    extra_context['post'] = post
    extra_context['answers'] = answers


class HotView(TemplateView):  # TODO: implement
    template_name = "index.html"
    extra_context = {}
    posts = []
    for i in range(0, 20):
        posts.append(Post)

    # tags = ['PostgreSQL', 'C++', 'Bootstrap', 'C', 'Python', 'Django', 'Boost']
    # best = ['Alice', 'Savva', 'Michael', 'Vladimir', 'Nikita', 'Tony']
    best = []
    for i in range(0, 6):
        best.append(User(nickname="User" + str(i)))

    tags = []
    for i in range(0, 6):
        tags.append(Tag(name="Tag"+str(i)))

    extra_context['tags'] = tags
    extra_context['best'] = best
    extra_context['posts'] = posts
    extra_context['mode'] = 'hot'


class TagView(TemplateView):  # TODO: implement
    template_name = "tag.html"
    extra_context = {}
    posts = []
    for i in range(0, 20):
        posts.append(Post)

    # tags = ['PostgreSQL', 'C++', 'Bootstrap', 'C', 'Python', 'Django', 'Boost']
    # best = ['Alice', 'Savva', 'Michael', 'Vladimir', 'Nikita', 'Tony']
    best = []
    for i in range(0, 6):
        best.append(User(nickname="User" + str(i)))
    tags = []
    for i in range(0, 6):
        tags.append(Tag(name="Tag"+str(i)))

    extra_context['tags'] = tags
    extra_context['best'] = best
    extra_context['posts'] = posts
    extra_context['tag'] = Tag(name="C++")


class AskView(TemplateView):  # TODO: implement
    template_name = "ask.html"


class SettingsView(TemplateView):  # TODO: implement
    template_name = "settings.html"

'''
############################################################################
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage
from django.views import View
from .models import *
from .forms import *

from ask_asysoev import settings

popular_tags = ['C++', 'Evangelion', 'Madoka',
                'C#', 'Троечку хочеться', 'Python']

best_members = ['Misha', 'Vova', 'Savva']

def paginate(objects, request, amount):
    paginator = Paginator(objects, amount)
    page = request.GET.get('page')
    return paginator.get_page(page)


class MainPage(View):
    template_name = 'index.html'

    def get(self, request):
        question_list = Question.objects.get_list()
        visible_questions = paginate(question_list, request, settings.QUEST_PER_PAGE)
        context = {'questions': visible_questions, 'popular_tags': popular_tags,
                   'best_members': best_members, 'user': request.user, 'mode': 'new'}
        return render(request, self.template_name, context)


class HotPage(View):
    template_name = 'index.html'

    def get(self, request):
        question_list = Question.objects.top()
        visible_questions = paginate(question_list, request, settings.QUEST_PER_PAGE)
        context = {'questions': visible_questions, 'popular_tags': popular_tags,
                   'best_members': best_members, 'user': request.user}
        return render(request, self.template_name, context)


class TagPage(View):
    template_name = 'tag.html'

    def get(self, request, tag_name):
        question_list = Question.objects.get_tag(tag_name)
        visible_questions = paginate(question_list, request, settings.QUEST_PER_PAGE)
        context = {'questions': visible_questions, 'popular_tags': popular_tags,
                   'best_members': best_members, 'user': request.user, 'tag_name': tag_name}
        return render(request, self.template_name, context)


class QuestionPage(View):
    template_name = 'question.html'
    form_class = CommentForm

    def get(self, request, question_id):
        main_question = Question.objects.get_question(question_id)
        answers = Answer.objects.answer(question_id)
        form = self.form_class()
        context = {'main_question': main_question, 'answers': answers,
                   'popular_tags': popular_tags, 'best_members': best_members,
                   'user': request.user, 'form': form}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, question_id):
        form = self.form_class(request.POST)
        if form.is_valid:
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = Question.objects.get_question(question_id)
            answer.save()
        return redirect('quest_page', question_id)


class SignupPage(View):
    template_name = 'signup.html'
    form_class = SignupForm

    def get(self, request):
        form = self.form_class()
        context = {'popular_tags': popular_tags,
                   'best_members': best_members,
                   'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.set_password(user.password)
            user.save()
            return redirect('login')
        context = {'popular_tags': popular_tags,
                   'best_members': best_members,
                   'form': form}
        return render(request, self.template_name, context)


class AskPage(View):
    template_name = 'ask.html'
    form_class = AskForm

    @method_decorator(login_required)
    def get(self, request):
        form = self.form_class()
        context = {'popular_tags': popular_tags,
                   'best_members': best_members,
                   'form': form}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid:
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            for tag in form['tag_list'].data.split():
                new_tag = Tag.objects.get_or_create(name=tag)
                print(new_tag)
                question.tags.add(new_tag[0])
            question.save()
            return redirect('quest_page', question_id=question.id)
        context = {'popular_tags': popular_tags,
                   'best_members': best_members,
                   'form': form}
        return render(request, self.template_name, context)


class SettingsPage(View):
    template_name = 'settings.html'
    form_class = SettingsForm

    @method_decorator(login_required)
    def get(self, request):
        form = self.form_class(instance=request.user)
        context = {'popular_tags': popular_tags,
                   'best_members': best_members,
                   'form': form}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request):
        form = self.form_class(request.POST, request.FILES, instance=request.user)
        if form.is_valid:
            user = form.save(commit=False)
            user.save()
        context = {'popular_tags': popular_tags,
                   'best_members': best_members,
                   'form': form}
        return render(request, self.template_name, context)


class LoginPage(View):
    template_name = "login.html"
