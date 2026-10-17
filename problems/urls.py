from django.urls import path
from . import views

urlpatterns = [
    path('', views.problem_list, name='problem_list'),

    path('report/', views.create_problem, name='create_problem'),

    path('<int:pk>/', views.problem_detail, name='problem_detail'),

    path(
        '<int:pk>/solution/',
        views.add_solution,
        name='add_solution'
    ),

    path(
        'solution/<int:pk>/vote/',
        views.vote_solution,
        name='vote_solution'
    ),
]