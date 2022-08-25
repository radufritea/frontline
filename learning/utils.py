from cgi import test
import zipfile
import os

from datetime import timedelta, date
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Course, Chapter, Lecture, Test, Question, CoursePermissions, TestPermission

today = date.today()


def get_course(pk):
    course = Course.objects.get(pk=pk)
    return course


def get_chapters(course):
    chapters = course.chapters.all().order_by("position")
    return chapters


def get_lectures(chapters):
    lectures = []
    for chapter in chapters:
        for lecture in chapter.lectures.all():
            lectures.append(lecture)

    return lectures


def get_course_duration(lectures):
    course_duration = timedelta(seconds=0)
    for lecture in lectures:
        course_duration += lecture.duration
    return course_duration


def get_active_courses_by_user(user):
    active_courses = CoursePermissions.objects.filter(
        user=user, start_date__lte=today, end_date__gte=today
    ).order_by("end_date")
    return active_courses


def get_history_courses_by_user(user):
    history_courses = CoursePermissions.objects.filter(user=user, end_date__lte=today).order_by(
        "end_date"
    )
    return history_courses


def get_active_courses_details(user):
    courses_details = {}
    active_permissions = get_active_courses_by_user(user)
    for permission in active_permissions:
        chapters = get_chapters(permission.course)
        lectures = get_lectures(chapters)
        duration = get_course_duration(lectures)
        no_of_lectures = len(lectures)
        # to do: compute accessed_lectures as no of lectures completed by user
        no_of_accessed_lectures = 0
        start_date = permission.start_date
        end_date = permission.end_date
        course_details = {
            permission.course.id: {
                "name": permission.course.name,
                "image": permission.course.thumbnail,
                "duration": duration,
                "no_of_lectures": no_of_lectures,
                "start_date": start_date,
                "end_date": end_date,
                "no_of_accessed_lectures": no_of_accessed_lectures,
            }
        }
        courses_details.update(course_details)
    return courses_details


def get_history_courses_details(user):
    history_courses_details = {}
    history_permissions = get_history_courses_by_user(user)

    for permission in history_permissions:
        chapters = get_chapters(permission.course)
        lectures = get_lectures(chapters)
        duration = get_course_duration(lectures)
        no_of_lectures = len(lectures)
        history_course_details = {
            permission.course.id: {
                "name": permission.course.name,
                "image": permission.course.thumbnail,
                "duration": duration,
                "no_of_lectures": no_of_lectures,
            }
        }
        history_courses_details.update(history_course_details)
    return history_courses_details


def get_course_counter(user):
    active_courses = get_active_courses_details(user)
    history_courses = get_history_courses_details(user)
    course_counter = len(active_courses.keys()) + len(history_courses.keys())
    return course_counter


def get_active_tests_by_user(user):
    active_tests = TestPermission.objects.filter(
        user=user, start_date__lte=today, end_date__gte=today
    ).order_by("end_date")
    return active_tests


def get_future_tests_by_user(user, page):
    future_tests = TestPermission.objects.filter(user=user, start_date__gt=today).order_by(
        "end_date"
    )
    paginator = Paginator(future_tests, 10)

    try:
        future_page_obj = paginator.page(page)
    except PageNotAnInteger:
        future_page_obj = paginator.page(1)
    except EmptyPage:
        future_page_obj = paginator.page(paginator.num_pages)
    return future_tests, future_page_obj


def get_history_tests_by_user(user, page):
    history_tests = TestPermission.objects.filter(user=user, end_date__lt=today).order_by(
        "end_date"
    )
    paginator = Paginator(history_tests, 10)

    try:
        history_page_obj = paginator.page(page)
    except PageNotAnInteger:
        history_page_obj = paginator.page(1)
    except EmptyPage:
        history_page_obj = paginator.page(paginator.num_pages)
    return history_tests, history_page_obj


def get_index_from_zip(lecture):
    lecture = Lecture.objects.get(id=lecture)
    file_name = lecture.zip_file
    folder_name = os.path.splitext(str(file_name))[0]
    dest_folder = "media/" + folder_name
    try:
        with zipfile.ZipFile(file_name, mode="r") as archive:
            archive.extractall(dest_folder)
            index = "/media/" + folder_name + "/index.html"
        return index
    except zipfile.BadZipFile as error:
        return "Acest exercitiu nu poate fi deschis. Va rugam sa ne sesizati aceasta eroare la adresa contact@frontlinesolutions.ro"


def get_test_details(pk):
    test = Test.objects.get(pk=pk)
    questions = Question.objects.filter(test=test)
    question_counter = range(1, test.questions_count + 1)
    test_choices_by_question = {}
    for question in questions:
        choices = question.choices.all()
        question_choices = {question.id: choices}
        test_choices_by_question.update(question_choices)
    return (questions, question_counter, test_choices_by_question)
