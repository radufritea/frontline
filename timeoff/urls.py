from django.urls import path
from .views import TimeoffDashboard

urlpatterns = [
    path('', TimeoffDashboard.as_view(), name='timeoff_dashboard')
]