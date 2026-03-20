import unittest
from app import create_app

class TestAmenityEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_amenity(self):
        """Test simple creation of an amenity"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "WiFi"
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['name'], "WiFi")

    def test_get_all_amenities(self):
        """Test retrieving the list of amenities"""
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.get_json(), list))

    def test_update_amenity(self):
        """Test updating an amenity name"""
        # Create one first
        res = self.client.post('/api/v1/amenities/', json={"name": "Air Con"})
        amenity_id = res.get_json()['id']

        # Update it
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "name": "Air Conditioning"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], "Amenity updated successfully")

    def test_create_invalid_amenity(self):
        """Test creation with empty name"""
        response = self.client.post('/api/v1/amenities/', json={"name": ""})
        self.assertEqual(response.status_code, 400)
