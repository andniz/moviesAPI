from rest_framework import generics, status
from rest_framework.response import Response
from .models import Movie, Comment
from .utils import OMDBException
from django.http import HttpResponseBadRequest, HttpResponseServerError, JsonResponse
from django.db.models import Count
from .serializers import MovieSerializer, CommentSerializer
from .utils import get_movie_details, rank_movies_by_comments


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
        return self.create(movie_details, *args, **kwargs)

    def create(self, data, *args, **kwargs):
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CommentsList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        movie_id = request.GET.get('movie_id', None)
        if movie_id is None:
            return self.list(request, *args, **kwargs)

        comments = Comment.objects.filter(movie_id=movie_id)
        serializer = self.get_serializer(comments, many=True)
        return JsonResponse(serializer.data, safe=False)


def top_commented_movies(request):
    begin_date = request.GET.get('begin_date', None)
    end_date = request.GET.get('end_date', None)
    if begin_date is None or end_date is None:
        return HttpResponseBadRequest('<h1>Please specify begin_date and end_date parameters in YYYY-MM-DD HH:MM format</h1>')
    movies = Movie.objects.filter(comments__published_date__range=(begin_date, end_date)).annotate(num_comments=Count('comments'))

    movies_without_comments = [m for m in Movie.objects.all() if m not in movies]
    movies_stats = [{'movie_id': movie.id, 'total_comments': movie.num_comments} for movie in movies]
    for i in movies_without_comments:
        movies_stats.append({'movie_id': i.id, 'total_comments': 0})
    movies_stats = rank_movies_by_comments(movies_stats)
    return JsonResponse(movies_stats, safe=False)
