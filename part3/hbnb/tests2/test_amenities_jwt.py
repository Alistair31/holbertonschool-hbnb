import unittest
from app import create_app, db

class TestAmenityJWT(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            # Création d'un admin pour tester (POST /amenities est souvent admin-only)
            from app.services import facade
            self.admin = facade.create_user({
                "first_name": "Admin", "last_name": "User",
                "email": "admin@test.com", "password": "adminpassword",
                "is_admin": True
            })

    def test_create_amenity_no_token(self):
        """Doit échouer (401) sans token"""
        response = self.client.post('/api/v1/amenities/', json={"name": "WiFi"})
        self.assertEqual(response.status_code, 401)

    def test_create_amenity_with_token(self):
        """Doit réussir (201) avec token admin"""
        # Login
        login_res = self.client.post('/api/v1/auth/login', 
                                    json={"email": "admin@test.com", "password": "adminpassword"})
        token = login_res.get_json()['access_token']
        
        # Create
        headers = {'Authorization': f'Bearer {token}'}
        response = self.client.post('/api/v1/amenities/', json={"name": "WiFi"}, headers=headers)
        self.assertEqual(response.status_code, 201)
