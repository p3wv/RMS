# from base64 import b64encode
# import unittest

# from flask import url_for
# from app import db
# from app.models import User, Role

# class APITestCase(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app('testing') # type: ignore
#         self.app_context = self.app.app_context()
#         self.app_context.push()
#         db.create_all()
#         Role.insert_roles()
#         self.client = self.app.test_client()

#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()
#         self.app_context.pop()


#     def get_api_headers(self, username, password):
#         return {
#             'Authorization' : 
#                 'Basic ' + b64encode(
#                     (username + ':' + password).encode('utf-8')).decode('utf-8'),
#             'Accept': 'application/json',
#             'Content-Type': 'application/json'
#         }
    
#     def test_no_auth(self):
#         response = self.client.get(url_for('api.get_posts'),
#                                    content_type='application/json')
#         self.assertEqual(response.status_code, 401)

#     def test_posts(self):
#         # add user
#         r = Role.query.filter_by(name='User').first()
#         self.assertIsNone(r)
#         u = User(email='')