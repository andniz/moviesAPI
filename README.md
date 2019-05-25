# moviesAPI

RESTful API project as part of the recruitment process for Python Developer position, written using Django and Django Rest Framework.

## Quickstart

To get the project up and running:

Download the files or fork the projects

Activate virtual environment

`pip install requirements.txt`

`python manage.py runserver`


## Available endpoints
### /movies
Supports POST and GET methods. 

POST method requires one and only one parameter - title. Data for the movie with given title will be
looked up via OMDBAPI and added to the application database. JSON containing the data of the movie will be
returned. If there is no title parameter or if more than one parameter is provided, server responds
with 400 Bad Request error. If the movie is not found through OMDBAPI, response status code should be
500 Internal Server Error.

GET method returns a list of movies in the database.

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

`url = 'http://127.0.0.1:8000  # Address if the server, in this example it's the localhost`

`response = requests.post(url + '/movies', data={'title': 'The Room'})`


TU WSTAWIC RESPONSE

`response2 = reuqests.get(url + '/movies)`

RESPONSE2

`response3 = requests.post(url + '/comments', data={'movie_id': 1, 'text': 'Oh hi Mark)`

RESPONSE3

`response4 = requests.get(url + '/comments', params={'movie_id': 1})`

RESPONSE4

`response5 = requests.get(url + '/top', params={'begin_date': '2019-04-02 20:30', 'end_date': '2019-04-02 22:00})`

RESPONSE5