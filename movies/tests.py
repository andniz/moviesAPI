from django.test import TestCase, RequestFactory
from .models import Movie, Comment
from .views import MoviesList
import json


class PostMovieTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_post_movie_params(self):
        req1 = self.factory.post('/movies')
        req2 = self.factory.post('/movies', data={'title': 'The Room', 'director': 'Tommy Wiseau'})
        req3 = self.factory.post('/movies', data={'title': 'Sharknado'})
        req4 = self.factory.post('/movies', data={'title': 'ahgsfds'})

        resp1 = MoviesList.as_view()(req1)
        resp2 = MoviesList.as_view()(req2)
        resp3 = MoviesList.as_view()(req3)
        resp4 = MoviesList.as_view()(req4)

        self.assertEqual(resp1.status_code, 400)
        self.assertEqual(resp2.status_code, 400)
        self.assertEqual(resp3.status_code, 201)
        self.assertEqual(resp4.status_code, 500)

    def test_basic_post_get_movie(self):
        req_post = self.factory.post('/movies', data={'title': 'Kung Fury'})
        resp_post = MoviesList.as_view()(req_post)
        req_get = self.factory.get('/movies')
        resp_get = MoviesList.as_view()(req_get)

        self.assertEqual(resp_post.data, resp_get.data[0])

