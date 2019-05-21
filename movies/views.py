from django.shortcuts import render
from rest_framework import generics
from .models import Movie, Comment
from .serializers import MovieSerializer, CommentSerializer
# Create your views here.


class MoviesList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def post(self, request, *args, **kwargs):
        pass
    # TODO: zdefiniować customowe zachowanie


class CommentsList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
