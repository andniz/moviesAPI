from django.urls import path
from . import views

urlpatterns = [
    path('movies', views.MoviesList.as_view()),
    path('comments', views.CommentsList.as_view()),
    path('top', views.top_commented_movies)
]