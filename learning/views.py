import random
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView


from .models import Lecture, Test, Card, BOXES, ResourceAccess
from .utils import (
    get_course,
    get_chapters,
    get_lectures,
    get_course_duration,
    get_active_courses_details,
    get_history_courses_details,
    get_course_counter,
    get_lecture_counter,
    get_permission_expiration_date,
    get_active_tests_by_user,
    get_index_from_zip,
    get_test_details,
    get_active_tests_by_user,
    get_future_tests_by_user,
    get_history_tests_by_user,
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
        context["course_counter"] = get_course_counter(self.request.user.id)
        context["lecture_counter"] = get_lecture_counter(self.request.user.id)
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
    ResourceAccess.objects.create(user=request.user, resource=pk, resource_type_id=1)
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

    permission_expiration_date = get_permission_expiration_date(user=request.user, course=course)
    context = {
        "course": course,
        "chapters": chapters,
        "lectures": lectures,
        "duration": duration,
        "flashcards": flashcards,
        "boxes": boxes,
        "card": card,
        "expiration_date": permission_expiration_date,
    }

    if request.method == "POST":
        form = CardCheckForm(request.POST)

        if form.is_valid():
            card = get_object_or_404(Card, id=form.cleaned_data["card_id"])
            card.move(form.cleaned_data["solved"])

        return redirect(request.META.get("HTTP_REFERER"))

    return render(request, "learning/course_detail.html", context)


class CourseUnavailable(TemplateView):
    template_name = "learning/course_unavailable.html"


class LectureDetailView(DetailView):
    model = Lecture
    template_name = "learning/lecture_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.request.GET.get("course")
        course = get_course(course_id)
        chapters = get_chapters(course)
        lectures = get_lectures(chapters)
        ResourceAccess.objects.create(
            user=self.request.user, resource=self.object.id, resource_type_id=2
        )

        if self.object.zip_file:
            index = get_index_from_zip(self.object.id)
        else:
            index = "None"

        context["course"] = course
        context["chapters"] = chapters
        context["lectures"] = get_lectures(chapters)
        context["duration"] = get_course_duration(lectures)
        context["index"] = index
        return context


class TestListView(ListView):
    template_name = "learning/test_list.html"
    paginate_by = 10
    context_object_name = "test_list"

    def get_queryset(self):
        test_list = get_active_tests_by_user(self.request.user)
        return test_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        future_tests, future_page_obj = get_future_tests_by_user(
            self.request.user, self.request.GET.get("page2")
        )
        history_tests, history_page_obj = get_history_tests_by_user(
            self.request.user, self.request.GET.get("page3")
        )
        context.update(
            {
                "future_tests": future_tests,
                "history_tests": history_tests,
                "future_page_obj": future_page_obj,
                "history_page_obj": history_page_obj,
            }
        )

        return context


class TestDetailView(DetailView):
    model = Test
    template_name = "learning/test_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions, question_counter, test_choices_by_question = get_test_details(self.object.id)
        context["questions"] = questions
        context["question_counter"] = question_counter
        context["choices"] = test_choices_by_question
        return context
