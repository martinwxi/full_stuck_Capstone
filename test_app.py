import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

assistant_token = "Bearer {}".format(os.environ.get('ASSISTANT_JWT'))
director_token = "Bearer {}".format(os.environ.get('DIRECTOR_JWT'))
producer_token = "Bearer {}".format(os.environ.get('PRODUCER_JWT'))

class CastingAgencyTestCase(unittest.TestCase):

  def setUp(self):
    self.app = create_app()
    self.client = self.app.test_client
    self.database_name = "casting_test"
    self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
    setup_db(self.app, self.database_path)

    # binds the app to the current context
    with self.app.app_context():
      self.db = SQLAlchemy()
      self.db.init_app(self.app)
      # create all tables
      self.db.create_all()

  def tearDown(self):
    """Executed after reach test"""
    pass

  #  Success behavior tests
  #  ----------------------------------------------------------------
  def test_get_actors (self):
    res = self.client().get('/actors', headers={ "Authorization": ( assistant_token ) })
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertTrue(data['success'])
    self.assertTrue(len(data['actors']) >= 0)

  def test_get_movies (self):
    res = self.client().get('/movies', headers={ "Authorization": ( assistant_token ) })
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertTrue(data['success'])
    self.assertTrue(len(data['movies']) >= 0)

  def test_create_actors (self):
    res = self.client().post('/actors', json=self.new_actor, headers={ "Authorization": ( director_token ) })
    data = json.loads(res.data)

    self.assertTrue(data['success'])
    self.assertTrue(len(data['actors']) == 1)

  def test_create_movies (self):
    res = self.client().post('/movies', json=self.new_movie, headers={ "Authorization": ( producer_token ) })
    data = json.loads(res.data)

    self.assertTrue(data['success'])
    self.assertTrue(len(data['movies']) == 1)

  def test_update_actors (self):
    self.client().post('/actors', json=self.new_actor, headers={ "Authorization": ( producer_token ) })
    res = self.client().patch('/actors/1', json=self.update_actor, headers={ "Authorization": ( producer_token ) })
    data = json.loads(res.data)

    self.assertTrue(data['success'])
    self.assertTrue(len(data['actors']) == 1)

  def test_update_movies (self):
    self.client().post('/movies', json=self.new_movie, headers={ "Authorization": ( director_token ) })
    res = self.client().patch('/movies/1', json=self.update_movie, headers={ "Authorization": ( director_token ) })
    data = json.loads(res.data)

    self.assertTrue(data['success'])
    self.assertTrue(len(data['movies']) == 1)

  def test_delete_actors (self):
    self.client().post('/actors', json=self.new_actor, headers={ "Authorization": ( producer_token ) })
    self.client().post('/actors', json=self.new_actor_2, headers={ "Authorization": ( producer_token ) })
    res = self.client().delete('/actors/2', headers={ "Authorization": ( producer_token ) })
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['delete'], '2')
    self.assertTrue(data['success'])

  def test_delete_movies (self):
    self.client().post('/movies', json=self.new_movie, headers={ "Authorization": ( producer_token ) })
    self.client().post('/movies', json=self.new_movie_2, headers={ "Authorization": ( producer_token ) })
    res = self.client().delete('/movies/2', headers={ "Authorization": ( producer_token ) })
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['delete'], '2')
    self.assertTrue(data['success'])

  #  Error behavior tests
  #  ----------------------------------------------------------------
  def test_401_get_actors (self):
    res = self.client().get('/actors')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 401)
    self.assertFalse(data['success'])

  def test_401_get_movies (self):
    res = self.client().get('/movies')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 401)
    self.assertFalse(data['success'])
  
  def test_401_create_actors (self):
    res = self.client().post('/actors', json=self.new_actor)
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 401)
    self.assertFalse(data['success'])

  def test_401_create_movies (self):
    res = self.client().post('/movies', json=self.new_movie)
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 401)
    self.assertFalse(data['success'])

  def test_404_update_actors (self):
    res = self.client().patch('/actors/1000', json=self.update_actor, headers={ "Authorization": ( producer_token ) })
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 404)
    self.assertFalse(data['success'])

  def test_404_update_movies (self):
    res = self.client().patch('/movies/1000', json=self.update_movie, headers={ "Authorization": ( producer_token ) })
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 404)
    self.assertFalse(data['success'])
  
  def test_404_delete_actors (self):
    res = self.client().delete('/actors/1000', headers={ "Authorization": ( producer_token ) })
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 404)
    self.assertFalse(data['success'])
  
  def test_404_delete_movies (self):
    res = self.client().delete('/movies/1000', headers={ "Authorization": ( producer_token ) })
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 404)
    self.assertFalse(data['success'])

# Make the tests conveniently executable
if __name__ == "__main__":
  unittest.main()