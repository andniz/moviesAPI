import requests
from movies_api.settings import OMDB_API_KEY


class OMDBException(Exception):
    pass


def get_movie_details(title):
    url = 'https://www.omdbapi.com/'
    params = {'t': title, 'apikey': OMDB_API_KEY}
    try:
        resp = requests.get(url, params)
    except ConnectionError:
        raise OMDBException('Connection error')
    dct = resp.json()
    if dct['Response'] == 'True':
        movie_details = dict()
        movie_details['title'] = dct['Title']  # Getting it from OMDB API for proper capitalization of words in title
        movie_details['year'] = dct['Year']
        movie_details['director'] = dct['Director']
        return movie_details
    else:
        raise OMDBException('Could not find the movie in the database')


def rank_movies_by_comments(movies_list):
    # movies_list: a list of dicts with movie_id and total_comments
    movies_list = sorted(movies_list, key=lambda m: m['total_comments'], reverse=True)
    rank = 0
    previous_comments = float('inf')
    for movie in movies_list:
        if movie['total_comments'] < previous_comments:
            rank += 1
        movie['rank'] = rank
        previous_comments = movie['total_comments']
    return movies_list
