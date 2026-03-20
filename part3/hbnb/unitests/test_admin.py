from unitests.base_test import BaseTestCase

class TestAmenity(BaseTestCase):
    def test_create_amenity_restricted_to_admin(self):
        """Verify RBAC: Non-admin users should get 403 when creating amenities."""
        user_token = self.create_and_login("user@hbnb.io", "pass123", is_admin=False)
        headers = {'Authorization': f'Bearer {user_token}'}
        
        response = self.client.post('/api/v1/amenities/', json={"name": "Pool"}, headers=headers)
        self.assertEqual(response.status_code, 403, "Regular users should be forbidden (403)")

    def test_create_amenity_admin_success(self):
        """Verify that an admin can successfully create an amenity."""
        admin_token = self.create_and_login("admin@hbnb.io", "admin123", is_admin=True)
        headers = {'Authorization': f'Bearer {admin_token}'}
        
        response = self.client.post('/api/v1/amenities/', json={"name": "WiFi"}, headers=headers)
        self.assertEqual(response.status_code, 201, "Admin should be able to create an amenity")
        self.assertEqual(response.get_json()['name'], "WiFi")
