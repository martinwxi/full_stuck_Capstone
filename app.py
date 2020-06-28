import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth
import datetime


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                        'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                        'GET,PUT,POST,DELETE,OPTIONS')
    return response

  #actor API
  @app.route('/actors')
  @requires_auth('get:actors')
  def get_all_actors(jwt):
    try:
      actors = Actor.query.all()
      actors_list = [actor.format() for actor in actors]
      return jsonify({
        'success': True,
        'actors': actors_list
        }), 200
    except Exception:
      abort(500)

  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def create_actor(jwt):
    try:
      data = request.get_json()
      name = data.get('name')
      age = data.get('age')
      gender = data.get('gender')
      actor = Actor(name=name, age=age, gender=gender)
      actor.insert()
      return jsonify({
        'success': True,
        'actors': actor.format()
        }), 200
    except Exception:
        abort(422)

  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def patch_actor(jwt, actor_id):
    data = request.get_json()
    name = data.get('name', None)
    age = data.get('age', None)
    gender = data.get('gender', None)
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    
    if actor is None:
      abort(404)

    if (not name) and (not age) and (not gender):
      abort(422)

    if name:
        actor.name = name
    if age:
        actor.age = age
    if gender:
        actor.gender = gender
    actor.update()

    return jsonify({
        'success': True,
        'actors': actor.format()
    }), 200


  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(jwt, actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    
    if not actor:
      abort(404)
    
    try:
      actor.delete()

      return jsonify({
          'success': True,
          'actors': actor_id
      }), 200

    except Exception:
      abort(422)

  #movie API
  @app.route('/movies')
  @requires_auth('get:movies')
  def get_all_movies(jwt):
      try:
        movies = Movie.query.all()
        movies_list = [movie.format() for movie in movies]
        return jsonify({
          'success': True,
          'movies': movies_list
          }), 200
      except Exception:
        abort(500)

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def create_movie(jwt):
      try:
        data = request.get_json()
        title = data.get('title')
        release_date = data.get('release_date')
        release_date = datetime.datetime.strptime(release_date, "%Y-%m-%d")
        movie = Movie(title=title, release_date=release_date)
        movie.insert()
        return jsonify({
          'success': True,
          'movies': movie.format()
          }), 200
      except Exception:
          abort(422)

  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(jwt, movie_id):
    data = request.get_json()
    title = data.get('title', None)
    release_date = data.get('release_date', None)
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

    if movie is None:
      abort(404)

    if (not title) and (not release_date):
      abort(422)

    if title:
      movie.title = title

    if release_date:
      try:
        release_date = datetime.datetime.strptime(release_date, "%Y-%m-%d")
        movie.release_date = release_date
      except Exception:
        abort(422)
    
    movie.update()

    return jsonify({
        'success': True,
        'movies': movie.format()
    }), 200


  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(jwt, movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    
    if not movie:
      abort(404)

    try:
      movie.delete()

      return jsonify({
          'success': True,
          'movies': movie_id
      }), 200

    except Exception:
      abort(422)

  #error code
  @app.errorhandler(405)
  def not_allowed(error):
      return jsonify({
          "success": False,
          "error": 405,
          "message": "Method not allowed"
      }), 405


  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          'success': False,
          'error': 400,
          'message': 'Bad request error'
      }), 400

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          'success': False,
          'error': 404,
          'message': 'Resource not found'
      }), 404

  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
          'success': False,
          'error': 500,
          'message': 'An error has occured, please try again'
      }), 500

  @app.errorhandler(422)
  def unprocesable_entity(error):
      return jsonify({
          'success': False,
          'error': 422,
          'message': 'Unprocessable entity'
      }), 422

  @app.errorhandler(AuthError)
  def handle_auth_error(exception):
      response = jsonify(exception.error)
      response.status_code = exception.status_code
      return response

  return app

app = create_app()

if __name__ == '__main__':
    app.run()