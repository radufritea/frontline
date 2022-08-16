import random
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, TemplateView


from .models import Course, Chapter, Lecture, Test, Card, BOXES
from .utils import (
    get_course,
    get_chapters,
    get_lectures,
    get_course_duration,
    get_active_courses_details,
    get_history_courses_details,
    get_active_tests_by_user,
    check_access,
    get_index_from_zip,
    get_test,
)
from .forms import CardCheckForm


class HomePageView(TemplateView):
    template_name = "index.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account_login")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        active_courses_details = get_active_courses_details(self.request.user.id)
        active_tests = get_active_tests_by_user(self.request.user.id)
        context["active_courses"] = active_courses_details
        context["active_tests"] = active_tests

        # Pagination
        active_courses = tuple(active_courses_details.items())
        page_courses = self.request.GET.get("page_courses", 1)
        page_tests = self.request.GET.get("page_tests", 1)
        paginator_courses = Paginator(active_courses, 10)
        paginator_tests = Paginator(active_tests, 10)

        try:
            page_obj_courses = paginator_courses.page(page_courses)
            page_obj_tests = paginator_tests.page(page_tests)
        except PageNotAnInteger:
            page_obj_courses = paginator_courses.page(1)
            page_obj_tests = paginator_tests.page(1)
        except EmptyPage:
            page_obj_courses = paginator_courses.page(paginator_courses.num_pages)
            page_obj_tests = paginator_tests.page(paginator_tests.num_pages)

        context["page_obj_courses"] = page_obj_courses
        context["page_obj_tests"] = page_obj_tests
        return context


def course_list(request):
    active_courses_details = get_active_courses_details(request.user.id)
    history_courses_details = get_history_courses_details(request.user.id)

    # Pagination
    active_courses = tuple(active_courses_details.items())
    history_courses = tuple(history_courses_details.items())
    page1 = request.GET.get("page1", 1)
    page2 = request.GET.get("page2", 1)
    paginator1 = Paginator(active_courses, 10)
    paginator2 = Paginator(history_courses, 10)

    try:
        page_obj_active = paginator1.page(page1)
        history_page_obj = paginator2.page(page2)
    except PageNotAnInteger:
        page_obj_active = paginator1.page(1)
        history_page_obj = paginator2.page(1)
    except EmptyPage:
        page_obj_active = paginator1.page(paginator1.num_pages)
        history_page_obj = paginator2.page(paginator2.num_pages)

    context = {
        "active_courses_details": active_courses_details,
        "page_obj_active": page_obj_active,
        "history_courses_details": history_courses_details,
        "history_page_obj": history_page_obj,
    }
    return render(request, "learning/course_list.html", context)


def course_detail(request, pk):
    course = get_course(pk)
    chapters = get_chapters(course)
    lectures = get_lectures(chapters)
    duration = get_course_duration(lectures)
    flashcards = Card.objects.filter(course=course.id).order_by("box", "-date_created")

    boxes = []
    for box_num in BOXES:
        card_count = Card.objects.filter(course=course.id).filter(box=box_num).count()
        boxes.append(
            {
                "number": box_num,
                "card_count": card_count,
            }
        )

    box_num = request.GET.get("box_num")
    cards_by_box = flashcards.filter(box=box_num)

    if cards_by_box:
        card = random.choice(cards_by_box)
    else:
        card = None

    context = {
        "course": course,
        "chapters": chapters,
        "lectures": lectures,
        "duration": duration,
        "flashcards": flashcards,
        "boxes": boxes,
        "card": card,
    }

    if request.method == "POST":
        form = CardCheckForm(request.POST)

        if form.is_valid():
            card = get_object_or_404(Card, id=form.cleaned_data["card_id"])
            card.move(form.cleaned_data["solved"])

        return redirect(request.META.get("HTTP_REFERER"))

    return render(request, "learning/course_detail.html", context)

    # if check_access(user, pk) == True:
    #     return render(request, 'learning/course_detail.html', context)
    # else:
    #     return redirect('course_unavailable')


def course_unavailable(request):
    return render(request, "learning/course_unavailable.html")


def lecture_detail(request, pk):
    course_id = request.GET.get("course")
    course = get_course(course_id)
    chapters = get_chapters(course)
    lectures = get_lectures(chapters)
    duration = get_course_duration(lectures)
    lecture = Lecture.objects.get(id=pk)

    if lecture.zip_file:
        index = get_index_from_zip(lecture.id)
    else:
        index = "None"

    context = {
        "course": course,
        "chapters": chapters,
        "lectures": lectures,
        "duration": duration,
        "lecture": lecture,
        "index": index,
    }
    return render(request, "learning/lecture_detail.html", context)


def test_list(request):
    test_list = Test.objects.all()
    page = request.GET.get("page", 1)
    paginator = Paginator(test_list, 10)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        "test_list": test_list,
        "page_obj": page_obj,
    }
    return render(request, "learning/test_list.html", context)


def test_detail(request, pk):
    test, questions = get_test(pk)
    question_counter = range(1, test.questions_count + 1)
    context = {
        "test": test,
        "questions": questions,
        "question_counter": question_counter,
    }
    return render(request, "learning/test_detail.html", context)
