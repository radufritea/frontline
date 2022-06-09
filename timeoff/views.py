from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


# Create your views here.
class TimeoffDashboard(TemplateView):
    template_name = 'timeoff_dashboard.html'