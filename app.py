import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
import datetime


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    return app

app = create_app()


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('/actors')
def get_actors(jwt):
    actors = Actor.query.all()
    if not actors:
        abort(404)

    actors_list = [actor.format() for actor in actors]

    return jsonify({
        'success': True,
        'actors': actors_list
    })


@app.route('/actors', methods=['POST'])
def add_actor(jwt):
    body = request.get_json()
    req_name = body.get('name')
    req_age = body.get('age')
    req_gender = body.get('gender')

    if not req_name:
        abort(422)

    actor = Actor(name=req_name, age=req_age, gender=req_gender)
    actor.insert()

    return jsonify({
        'success': True,
        'actors': actor.format()
    })


@app.route('/actors/<id>', methods=['PATCH'])
def update_actor(jwt, id):
    body = request.get_json()
    req_name = body.get('name')
    req_age = body.get('age')
    req_gender = body.get('gender')
    if (not req_name) and (not req_age) and (not req_gender):
        abort(422)

    actor = Actor.query.filter(Actor.id == id).one_or_none()
    if not actor:
        abort(404)
    if req_name:
        actor.name = req_name
    if req_age:
        actor.age = req_age
    if req_gender:
        actor.gender = req_gender
    actor.update()

    return jsonify({
        'success': True,
        'actors': actor.format()
    })


@app.route('/actors/<id>', methods=['DELETE'])
def delete_actor(jwt, id):
    actor = Actor.query.filter(Actor.id == id).one_or_none()
    if not actor:
        abort(404)
    actor.delete()

    return jsonify({
        'success': True,
        'actors': id
    })


@app.route('/movies')
def get_movies(jwt):
    movies = Movie.query.all()
    if not movies:
        abort(404)

    movies_list = [movie.format() for movie in movies]

    return jsonify({
        'success': True,
        'movies': movies_list
    })


@app.route('/movies', methods=['POST'])
def add_movie(jwt):
    body = request.get_json()
    req_title = body.get('title')
    req_release_date = body.get('release_date')
    release_date = datetime.datetime.strptime(req_release_date, "%Y-%m-%d")

    if not req_title:
        abort(422)

    movie = Movie(title=req_title, release_date=release_date)
    movie.insert()

    return jsonify({
        'success': True,
        'movies': movie.format()
    })


@app.route('/movies/<id>', methods=['PATCH'])
def update_movie(jwt, id):
    body = request.get_json()
    req_title = body.get('title')
    req_release_date = body.get('release_date')
    if (not req_title) and (not req_release_date):
        abort(422)
    release_date = datetime.datetime.strptime(req_release_date, "%Y-%m-%d")

    movie = Movie.query.filter(Movie.id == id).one_or_none()
    if not movie:
        abort(404)
    if req_title:
        movie.title = req_title
    if req_release_date:
        movie.release_date = release_date
    movie.update()

    return jsonify({
        'success': True,
        'movies': movie.format()
    })


@app.route('/movies/<id>', methods=['DELETE'])
def delete_movie(jwt, id):
    movie = Movie.query.filter(Movie.id == id).one_or_none()
    if not movie:
        abort(404)
    movie.delete()

    return jsonify({
        'success': True,
        'movies': id
    })


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(405)
def not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method not allowed"
    }), 405


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Server error"
    }), 500

if __name__ == '__main__':
    app.run()