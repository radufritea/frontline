from django.urls import path
from .views import HomePageView

from . import views

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("courses/course-list/", views.course_list, name="course_list"),
    path("courses/<int:pk>/", views.course_detail, name="course_detail"),
    path("courses/unavailable/", views.course_unavailable, name="course_unavailable"),
    path("courses/lectures/<int:pk>/", views.lecture_detail, name="lecture_detail"),
    path("tests/test_list/", views.test_list, name="test_list"),
    path("tests/<int:pk>/", views.test_detail, name="test_detail"),
]
