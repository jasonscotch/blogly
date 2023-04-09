from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users"""
    
    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="TestFirst", last_name='TestLast', image_url='https://cdn.pixabay.com/photo/2020/07/01/12/58/icon-5359553_1280.png')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()
        
    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirst', html)
    
    def test_homepage_redirect(self):
        with app.test_client() as client:
            resp = client.get('/')
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, 'http://localhost/users')
            
    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'TestFirst TestLast', resp.data)
            
    def test_show_edit_user(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/edit')
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'TestFirst', resp.data)
            self.assertIn(b'TestLast', resp.data)
            
    def test_create_user(self):
        with app.test_client() as client:
            d = {"First Name": "New", "Last Name": "User", "Image URL": ""}
            resp = client.post('/users/new', data=d, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'New User', resp.data)
            
    def test_edit_user(self):
        with app.test_client() as client:
            d = {"First Name": "Changed", "Last Name": "Name", "Image URL": ""}
            resp = client.post(f'/users/{self.user_id}/edit', data=d, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'Changed Name', resp.data)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/delete', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(b'Test User', resp.data)