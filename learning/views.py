from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


# Create your views here.
class CoursesListView(TemplateView):
    template_name = 'courses_list.html'