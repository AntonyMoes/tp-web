from django.contrib import admin

from .models import *

from django.contrib.contenttypes.admin import GenericStackedInline


class ProfileAdmin(admin.ModelAdmin):
    fields = ['nickname', 'username', 'password', 'avatar_path', 'email']


class LikeInlineAdmin(GenericStackedInline):
    model = LikeDislike


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    filter_horizontal = ('tags',)
    inlines = [LikeInlineAdmin]


class AnswerAdmin(admin.ModelAdmin):
    model = Question
    inlines = [LikeInlineAdmin]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Tag)
admin.site.register(Profile, ProfileAdmin)


