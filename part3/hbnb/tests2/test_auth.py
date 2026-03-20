import unittest
from app import create_app, db
from app.models.user import User

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = create_app('app.config.DevelopmentConfig') # Ou une config de Test
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_and_login(self):
        # 1. Création de l'utilisateur (avec password !)
        user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@hbnb.com",
            "password": "securepassword123"
        }
        # Note: Dans ton code actuel, POST /users/ est restreint aux admins
        # Tu devras peut-être créer l'utilisateur via la facade pour ce test
        from app.services import facade
        with self.app.app_context():
            facade.create_user(user_data)

        # 2. Test du Login
        login_data = {"email": "test@hbnb.com", "password": "securepassword123"}
        response = self.client.post('/api/v1/auth/login', json=login_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.get_json())
