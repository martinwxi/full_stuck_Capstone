# Casting-Agency-Specifications

## Motivation for project
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

### Models:

Movies with attributes title and release date

Actors with attributes name, age and gender

### Endpoints:

GET /actors and /movies

DELETE /actors/ and /movies/

POST /actors and /movies and

PATCH /actors/ and /movies/

### Roles:

Casting Assistant

Can view actors and movies

Casting Director

All permissions a Casting Assistant has and…

Add or delete an actor from the database

Modify actors or movies

Executive Producer

All permissions a Casting Director has and…

Add or delete a movie from the database

### Tests:

One test for success behavior of each endpoint

One test for error behavior of each endpoint

At least two tests of RBAC for each role


## Getting Started

### Installing Dependencies

#### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
When testing locally, models.py should be:
```python
# database_path = os.environ['DATABASE_URL']

database_name = "casting"
database_path = "postgresql://martin@{}/{}".format('localhost:5432', database_name)
```
When testing on heroku, models.py should be:
```python
database_path = os.environ['DATABASE_URL']

#database_name = "casting"
#database_path = "postgresql://martin@{}/{}".format('localhost:5432', database_name)
```

we can run our local migrations using our manage.py file, to mirror how Heroku will run behind the scenes for us when we deploy our application:
```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

## Running the server locally

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
Setting the FLASK_ENV variable to development will detect file changes and restart the server automatically.

## Running the server on heroku

I already deployed the API in heroku and can test it directly. The host is:

https://castingapi.herokuapp.com/

The token is in the `setup.sh`, you can test the API like this:

```bash
source setup.sh
curl -H "Authorization: Bearer ${assistant_token}" https://castingapi.herokuapp.com/actors | jq
```


## API document

### Endpoints
```
GET '/actors'
POST '/actors'
PATCH '/actors/<int:actor_id>'
DELETE '/actors/<int:actor_id>'
GET '/movies'
POST '/movies'
PATCH '/movies/<int:movie_id>'
DELETE '/movies/<int:movie_id>'
```

#### GET '/actors'
- Get the information of all actors
- Request Arguments: None
- Returns: A list contains the information of all actors.
```
{
  "actors": {
    "age": 23,
    "gender": "female",
    "id": 8,
    "name": "SA Potter"
  },
  "success": true
}
```
#### POST '/actors'
- Create an actor
- Request Arguments: name, age, gender
{"name":"actor1", "age":20, "gender":"female"}
- Returns: The actor information which we added with this request.
```
{
  "actors": {
    "age": 20,
    "gender": "female",
    "id": 9,
    "name": "actor1"
  },
  "success": true
}
```
#### PATCH '/actors/<int:actor_id>'
- Update the actor information
- Request Arguments: name, age, gender
{"name":"actor2", "age":30, "gender":"female"}
- Returns: The actor information which we updated with this request.
```
{
  "actors": {
    "age": 30,
    "gender": "female",
    "id": 9,
    "name": "actor2"
  },
  "success": true
}
```
#### DELETE '/actors/<int:actor_id>'
- Delete an actor
- Returns: The id of the actor which was deleted 
```
{
  "actors": "1",
  "success": true
}
```
#### GET '/movies'
- Get the information of all movies
- Request Arguments: None
- Returns: A list contains the information of all movies.
```
{
  "movies": [
    {
      "id": 1,
      "release_date": "2000-01-01",
      "title": "Harry Porter"
    }
  ],
  "success": true
}
```
#### POST '/movies'
- Create a movie
- Request Arguments: title, release_date
{"title":"movie1", "release_date": "2010-1-1"}
- Returns: The movie information which we added with this request.
```
{
  "movies": {
    "id": 2,
    "release_date": "2010-1-1",
    "title": "movie1"
  },
  "success": true
}
```
#### PATCH '/movies/<int:movie_id>'
- Update movie information
- Request Arguments: title, release_date
{"title":"movie2", "release_date": "2019-1-1"}
- Returns: The movie info which we updated with this request.
```
{
  "movies": {
    "id": 2,
    "release_date": "2019-1-1",
    "title": "movie2"
  },
  "success": true
}
```
#### DELETE '/movies/<int:movie_id>'
- Delete a movie
- Returns: The id of the movie which was deleted 
```
{
  "movies": "1",
  "success": true
}
```

## Testing
To run the tests locally, run

```bash
dropdb casting_test
createdb casting_test
psql casting_test < casting.psql
python test_app.py
```
