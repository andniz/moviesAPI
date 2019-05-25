# moviesAPI

RESTful API project as part of the recruitment process for Python Developer position, written using Django and Django Rest Framework.

## Quickstart

To get the project up and running:

Download the files or fork the projects

Activate virtual environment

`pip install -r requirements.txt`

`python manage.py runserver`


## Available endpoints
### /movies
Supports POST and GET methods. 

POST method requires one and only one parameter - title. Data for the movie with given title will be
looked up via OMDBAPI and added to the application database. JSON containing the data of the movie will be
returned. If there is no title parameter or if more than one parameter is provided, server responds
with 400 Bad Request error. If the movie is not found through OMDBAPI, response status code should be
500 Internal Server Error.

GET method returns a list of movies in the database. Providing the ordering parameter with a value of 
year or title will make the resulting JSON be sorted by the value. Providing the value with a minus 
sign before it (ie. -title, -year) will reverse the sorting.

### /comments
Supports POST and GET methods.

POST method requires parameters of movie_id (referring to the movie being commented) and text, with
the body of the comment. If any of these parameters is not provided, the server responds with
400 Bad Request error message.

GET method accepts movie_id parameter. If it is given, the server returns a list of comments related to
the movie with the given ID. If not, it returns a list of all the comments in the database. 

### /top
Only supports the GET method. 

GET method requires parameters of begin_date and end_date, both in format of 'YYYY-MM-DD HH:MM'.
The server returns a list of movies, ranked by the number of comments within the given time range.

## Example usage
`import requests`

`url = 'http://127.0.0.1:8000  # Address of the server, in this example it's the localhost`

POST /movies:

`response = requests.post(url + '/movies', data={'title': 'The Room'})`

JSON Response:

`{
    "id": 5,
    "title": "The Room",
    "year": 2003,
    "director": "Tommy Wiseau"
}`

GET /movies:

`response2 = reuqests.get(url + '/movies)`

`[
    {
        "id": 1,
        "title": "Sharknado",
        "year": 2013,
        "director": "Anthony C. Ferrante"
    },
    {
        "id": 2,
        "title": "the room",
        "year": 2003,
        "director": "Tommy Wiseau"
    },
    {
        "id": 3,
        "title": "rubber",
        "year": 2010,
        "director": "Quentin Dupieux"
    },
    {
        "id": 4,
        "title": "Shrek 2",
        "year": 2004,
        "director": "Andrew Adamson, Kelly Asbury, Conrad Vernon"
    },
    {
        "id": 5,
        "title": "The Room",
        "year": 2003,
        "director": "Tommy Wiseau"
    }
]`

POST /comments:

`response3 = requests.post(url + '/comments', data={'movie_id': 1, 'text': 'Oh hi Mark'})`

`{
    "id": 6,
    "text": "Oh hi Mark",
    "movie_id": 5,
    "published_date": "2019-05-25T21:14:07.645327Z"
}`

GET /top

`response4 = requests.get(url + '/top', params={'begin_date': '2019-04-02 20:30', 'end_date': '2019-04-02 22:00})`

`[
    {
        "movie_id": 1,
        "total_comments": 2,
        "rank": 1
    },
    {
        "movie_id": 2,
        "total_comments": 2,
        "rank": 1
    },
    {
        "movie_id": 3,
        "total_comments": 0,
        "rank": 2
    },
    {
        "movie_id": 4,
        "total_comments": 0,
        "rank": 2
    },
    {
        "movie_id": 5,
        "total_comments": 0,
        "rank": 2
    }
]`