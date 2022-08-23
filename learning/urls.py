from django.urls import path
from .views import HomePageView, CourseUnavailable, LectureDetailView, TestDetailView, TestListView

from . import views

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("courses/course-list/", views.course_list, name="course_list"),
    path("courses/<int:pk>/", views.course_detail, name="course_detail"),
    path("courses/unavailable/", CourseUnavailable.as_view(), name="course_unavailable"),
    path("courses/lectures/<int:pk>/", LectureDetailView.as_view(), name="lecture_detail"),
    path("tests/test_list/", TestListView.as_view(), name="test_list"),
    path("tests/<int:pk>/", TestDetailView.as_view(), name="test_detail"),
]
