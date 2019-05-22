from rest_framework import generics, status
from rest_framework.response import Response
from .models import Movie, Comment
from .utils import OMDBException
from django.http import HttpResponseBadRequest, HttpResponseServerError, JsonResponse
from django.db.models import Count
from .serializers import MovieSerializer, CommentSerializer
from .utils import get_movie_details, rank_movies_by_comments
# Create your views here.


class MoviesList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def post(self, request, *args, **kwargs):
        title = request.data.get('title', None)
        if title is None or len(list(request.data.keys())) > 1:
            return HttpResponseBadRequest('<h1>Please provide the title parameter (and only it).</h1>')

        try:
            movie_details = get_movie_details(title)
        except OMDBException as err:
            return HttpResponseServerError(f'<h1>{err.args[0]}</h1>')
        movie_details['title'] = title
        return self.create(movie_details, *args, **kwargs)

    def create(self, dict, *args, **kwargs):
        serializer = self.get_serializer(data=dict)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CommentsList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


def top_commented_movies(request):
    movies = Movie.objects.all().annotate(num_comments=Count('comments'))
    movies_stats = [{'movie_id': movie.id, 'total_comments': movie.num_comments} for movie in movies]
    movies_stats = rank_movies_by_comments(movies_stats)
    return JsonResponse(movies_stats, safe=False)

