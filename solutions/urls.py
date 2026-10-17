from django.urls import path
from . import views

urlpatterns = [
    path(
        'problem/<int:problem_id>/add/',
        views.add_solution,
        name='add_solution'
    ),
    path(
        '<int:solution_id>/vote/',
        views.vote_solution,
        name='vote_solution'
    ),
]