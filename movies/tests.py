from django.test import TestCase, RequestFactory
from .models import Movie, Comment
from .views import MoviesList, CommentsList, top_commented_movies
import json


class PostMoviesTestCase(TestCase):
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


class PostCommentsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        req = self.factory.post('/movies', data={'title': 'Sharknado'})
        resp = MoviesList.as_view()(req)

    def test_post_comment_movie_id(self):
        req1 = self.factory.post('/comments', data={'text': 'Great movie'})
        req2 = self.factory.post('/comments', data={'movie_id': 1, 'text': 'Meh/10'})
        req3 = self.factory.post('/comments', data={'movie_id': 6, 'text': 'Best one ever'})

        resp1 = CommentsList.as_view()(req1)
        resp2 = CommentsList.as_view()(req2)
        resp3 = CommentsList.as_view()(req3)

        self.assertEqual(resp1.status_code, 400)
        self.assertEqual(resp2.status_code, 201)
        self.assertEqual(resp3.status_code, 400)


class GetCommentsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        Movie.objects.create(title='The Room', year=2003, director='Tommy Wiseau')
        Movie.objects.create(title='Sharknado', year=2013, director='Anthony C. Ferrante')
        Movie.objects.create(title='Rubber', year=2010, director='Quentin Dupieux')
        Movie.objects.create(title='Kung Fury', year=2015, director='David Sandberg')
        Comment.objects.create(movie_id_id=1, text='Lorem ipsum', published_date='2017-05-23 22:01')
        Comment.objects.create(movie_id_id=1, text='Lorem ipsum', published_date='2019-04-02 15:16')
        Comment.objects.create(movie_id_id=4, text='Lorem ipsum', published_date='2018-08-19 08:15')
        Comment.objects.create(movie_id_id=4, text='Lorem ipsum', published_date='2018-12-17 19:52')
        Comment.objects.create(movie_id_id=2, text='Lorem ipsum', published_date='2018-11-05 23:17')
        Comment.objects.create(movie_id_id=3, text='Lorem ipsum', published_date='2018-04-02 09:12')

    def test_top_comments(self):
        """Only takes comments in the date range into account and properly ranks movies"""
        req = self.factory.get('/top', {'begin_date': '2018-01-01 00:01', 'end_date': '2018-12-31 23:59'})
        resp = top_commented_movies(req)
        resp_list = json.loads(resp.content)
        self.assertEqual(resp_list[0], {'movie_id': 4, 'total_comments': 2, 'rank': 1})
        self.assertEqual(resp_list[1]['total_comments'], 1)
        self.assertEqual(resp_list[1]['rank'], 2)
        self.assertEqual(resp_list[2]['total_comments'], 1)
        self.assertEqual(resp_list[2]['rank'], 2)
        self.assertEqual(resp_list[3], {'movie_id': 1, 'total_comments': 0, 'rank': 3})
