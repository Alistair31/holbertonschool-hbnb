from unitests.base_test import BaseTestCase

class TestAuth(BaseTestCase):
    def test_login_success(self):
        """Verify that a registered user can login and receive a valid JWT."""
        from app.services import facade
        facade.create_user({"first_name": "John", "last_name": "Doe", 
                           "email": "john@hbnb.io", "password": "secure123"})

        login_data = {"email": "john@hbnb.io", "password": "secure123"}
        response = self.client.post('/api/v1/auth/login', json=login_data)
        
        self.assertEqual(response.status_code, 200, "Should return 200 OK")
        self.assertIn('access_token', response.get_json(), "Response must contain a JWT token")

    def test_login_invalid_credentials(self):
        """Ensure that wrong passwords return 401 Unauthorized."""
        login_data = {"email": "fake@hbnb.io", "password": "wrong"}
        response = self.client.post('/api/v1/auth/login', json=login_data)
        self.assertEqual(response.status_code, 401, "Should fail with 401")
