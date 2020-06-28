import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

assistant_token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImYxa1lCd3kwV2hpZkQtNkd2OFRWZiJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHlwcm9qZWN0LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWViZDEwNGFlMzZkNjAwMTk2YTI2NWQiLCJhdWQiOiJ0ZXN0IiwiaWF0IjoxNTkzMzc4MjAwLCJleHAiOjE1OTMzODU0MDAsImF6cCI6IkxJWEZyYmdrWDdKNVNoS041NzNtbWZQMDBZa2F1MHFKIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.Ttk2qcMw7JtZTG6TO5EXvkIOkVhFVSf_3G1fXzuGsqDDKvrDNMZZT6ECP9VapAhPklSdCTUY2LB-7T7QzKj_9xUTPHwY4m6a2IN-dX1oDyKJFqFKdQXed4gOxRJax2F5LljnXlRpIIHDwpOzBvenlOCuM_P6TF4CZeAjffYCmIfEuapHSIFk1YUG68r7Cg5axzBRL4Pz6jwBDxTPvKuTtEtR_sLTA273_E8bZS0hGxf7jaOD6SyGD5Y2OtI-rdiJL5vg94Mm90RbnQt3RV7zKbfU0hgyJU0knLaHbOyc2jxcWPUbEvV9Kyw9bk8iH7gplTtVaj9gyk6jJBuiXyNPlw"
director_token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImYxa1lCd3kwV2hpZkQtNkd2OFRWZiJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHlwcm9qZWN0LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWU5YzdiOWI4YTY1OTAwMTllNGZmMDQiLCJhdWQiOiJ0ZXN0IiwiaWF0IjoxNTkzMzc3OTk3LCJleHAiOjE1OTMzODUxOTcsImF6cCI6IkxJWEZyYmdrWDdKNVNoS041NzNtbWZQMDBZa2F1MHFKIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.AbDfEUMn0M-Iv5_Zm8yACNmhyLTNPfmB2L6g-QmsSJx2sa1CB5Hyd1CGjKMc5rN_26h9PVZcA-n-nu536XTLAZpf-c4Y2ojwvkVyjdZ398wH9s5UDXpw8WfqeZq3CdY_Lci0H5ySsL4oCHoH63_8np778GPs-AGyfIWR-m0i-fE-5lE3Zt9w9d6IjETtUWBv3NFH5MDV23Bsny7cVw6E55HRGp7pJfKlwwhe_QwCqvTBNR8XN1yCI-Z7JvbIDEEUUuXVHVt6tZhNtjn7oo_eLcFMfrsfoRfmOMvSLKg3N124l_ChT_6K1S-7zav0QqdFJnMlE_ciHdifRep-FVdXhA"
producer_token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImYxa1lCd3kwV2hpZkQtNkd2OFRWZiJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHlwcm9qZWN0LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWY5MDJkZWVmMGRhMTAwMTM0YWEwYWQiLCJhdWQiOiJ0ZXN0IiwiaWF0IjoxNTkzMzc3OTEyLCJleHAiOjE1OTMzODUxMTIsImF6cCI6IkxJWEZyYmdrWDdKNVNoS041NzNtbWZQMDBZa2F1MHFKIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.PSEo9UHT3cU22M-cxJFaK8-3xpuTAwUDUMY5TQWdUimp3M4PUUTtUz4DgHpjwvE_OGoRTLX7X5_A3kSWqUwQaNfsuwSfyGX3px9TolNvQvYJigeKggpa_p0Mp1H6_CkpxPhWcu-oVfTU2VPGGrW0MdYPTMsS-qsPMmPD2SF6CkVHw9Ft1J1TGXe2gNzIkyzjIP6Ve157QGw7VkhRdjMC2rN3CD1kk4L8nHJ-fi3hC8US0eodXOEI3Tx1Yq6Q9oWWCWf7f4iIvYLYdLBLYH5gCaOPnmz_4X3-3aabwSr9u4J-YvO-v_16Zcc_ChZeGIgyNr3uLupyqBnwPY_5hF52oQ"

class CastingAgencyTestCase(unittest.TestCase):

  def setUp(self):
    self.app = create_app()
    self.client = self.app.test_client
    self.database_name = "casting_test"
    self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
    setup_db(self.app, self.database_path)

    self.new_actor = {
      'name': 'Harry 1',
      'age': 21,
      'gender': 'Male'
    }

    self.new_actor_2 = {
      'name': 'Harry 2',
      'age': 22,
      'gender': 'Female'
    }

    self.update_actor = {
      'name': 'Harry 3',
      'age': 23,
      'gender': 'Female'
    }

    self.new_movie = {
      'title': 'Harry Portter 1',
      'release_date': '2020-1-1'
    }

    self.new_movie_2 = {
      'title': 'Harry Portter 2',
      'release_date': '2020-1-1'
    }

    self.update_movie = {
      'title': 'Harry Portter 3',
      'release_date': '2021-1-1'
    }

    with self.app.app_context():
        self.db = SQLAlchemy()
        self.db.init_app(self.app)
        self.db.create_all()

  def tearDown(self):
    """Executed after reach test"""
    pass

  #  Success tests
  def test_get_all_actors (self):
    res = self.client().get('/actors', headers={ "Authorization": assistant_token})
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertTrue(data['success'])
    self.assertTrue(len(data['actors']) >= 0)

  def test_get_all_movies (self):
    res = self.client().get('/movies', headers={ "Authorization": ( assistant_token ) })
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertTrue(data['success'])
    self.assertTrue(len(data['movies']) >= 0)

  def test_create_actors (self):
    res = self.client().post('/actors', json=self.new_actor, headers={ "Authorization": ( director_token ) })
    data = json.loads(res.data)

    self.assertTrue(data['success'])
    self.assertTrue(len(data['actors']) >= 1)

  def test_create_movies (self):
    res = self.client().post('/movies', json=self.new_movie, headers={ "Authorization": ( producer_token ) })
    data = json.loads(res.data)

    self.assertTrue(data['success'])
    self.assertTrue(len(data['movies']) >= 1)

  def test_update_actors (self):
    self.client().post('/actors', json=self.new_actor, headers={ "Authorization": ( producer_token ) })
    res = self.client().patch('/actors/1', json=self.update_actor, headers={ "Authorization": ( producer_token ) })
    data = json.loads(res.data)

    self.assertTrue(data['success'])
    self.assertTrue(len(data['actors']) >= 1)

  def test_update_movies (self):
    self.client().post('/movies', json=self.new_movie, headers={ "Authorization": ( director_token ) })
    res = self.client().patch('/movies/1', json=self.update_movie, headers={ "Authorization": ( director_token ) })
    data = json.loads(res.data)

    self.assertTrue(data['success'])
    self.assertTrue(len(data['movies']) >= 1)

  def test_delete_actors (self):
    self.client().post('/actors', json=self.new_actor, headers={ "Authorization": ( producer_token ) })
    self.client().post('/actors', json=self.new_actor_2, headers={ "Authorization": ( producer_token ) })
    res = self.client().delete('/actors/8', headers={ "Authorization": ( producer_token ) })
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertTrue(data['success'])

  def test_delete_movies (self):
    self.client().post('/movies', json=self.new_movie, headers={ "Authorization": ( producer_token ) })
    self.client().post('/movies', json=self.new_movie_2, headers={ "Authorization": ( producer_token ) })
    res = self.client().delete('/movies/3', headers={ "Authorization": ( producer_token ) })
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertTrue(data['success'])

  #  Error tests
  def test_unauthorized_get_actors (self):
    res = self.client().get('/actors')

    self.assertEqual(res.status_code, 401)

  def test_unauthorized_get_movies (self):
    res = self.client().get('/movies')

    self.assertEqual(res.status_code, 401)
  
  def test_unauthorized_create_actors (self):
    res = self.client().post('/actors', json=self.new_actor)

    self.assertEqual(res.status_code, 401)

  def test_unauthorized_create_movies (self):
    res = self.client().post('/movies', json=self.new_movie)

    self.assertEqual(res.status_code, 401)

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