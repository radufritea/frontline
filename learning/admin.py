from django.contrib import admin
from nested_admin import NestedTabularInline, NestedModelAdmin

from .models import Course, Chapter, Lecture, LectureType, CourseCategory, CoursePermissions, Card, Question, Test, Choice, UserChoice, TestInstance


class ChoicesInline(NestedTabularInline):
	model = Choice
	extra = 4
	max_num = 4

class QuestionInline(NestedTabularInline):
	model = Question 
	inlines = [ChoicesInline,]
	extra = 10
	list_display = ("label", "feedback", "order",)

class TestAdmin(NestedModelAdmin):
	inlines = [QuestionInline,]


# class UserChoiceInline(admin.TabularInline):
# 	model = UserChoice

# class TestInstanceAdmin(admin.ModelAdmin):
# 	inlines = [UserChoiceInline,]


admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Lecture)
admin.site.register(CourseCategory)
admin.site.register(CoursePermissions)
admin.site.register(Card)
admin.site.register(LectureType)
admin.site.register(Test, TestAdmin)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(UserChoice)
admin.site.register(TestInstance)