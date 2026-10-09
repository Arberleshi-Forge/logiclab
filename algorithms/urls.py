from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="algorithms_dashboard"),
    path("complexity/", views.complexity_view, name="complexity_analyzer"),
    path("sorting/", views.sorting_view, name="sorting_visualizer"),
    path("recursion/", views.recursion_view, name="recursion_demo"),
    path("theory/", views.theory_view, name="algorithm_theory"),
]
