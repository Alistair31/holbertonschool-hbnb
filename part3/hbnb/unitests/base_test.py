import unittest
from app import create_app, db
from app.services import facade
from app.config import TestingConfig

# ATTENTION : Il n'y a PAS de ligne "from unitests.base_test import BaseTestCase" ici.

class BaseTestCase(unittest.TestCase):
    """Base class for all HBNB unit tests to ensure environment isolation."""

    def setUp(self):
        # On passe directement la classe (pas de guillemets !)
        self.app = create_app(TestingConfig) 
        
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_and_login(self, email, password, is_admin=False):
        """Helper to create a user and return their access token."""
        facade.create_user({
            "first_name": "Test", "last_name": "User",
            "email": email, "password": password, "is_admin": is_admin
        })
        resp = self.client.post('/api/v1/auth/login', json={"email": email, "password": password})
        return resp.get_json().get('access_token')