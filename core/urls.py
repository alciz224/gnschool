from os import path
from django.urls import path

from core.views import HomeView

urlpatterns=[
        path("", HomeView.as_view(), name="home"),

        ]
