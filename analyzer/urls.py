from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("analyzer/", views.analyzer, name="analyzer"),
    path("result/", views.result, name="result"),
    path("about/", views.about, name="about"),
]
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("analyzer/", views.analyzer, name="analyzer"),
    path("result/", views.result, name="result"),
    path("history/", views.history, name="history"),
]
