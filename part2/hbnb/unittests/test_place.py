import unittest
import uuid
from app import create_app


class TestPlaceEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        unique_email = f"owner_{uuid.uuid4().hex[:8]}@test.com"

        user_res = self.client.post('/api/v1/users/', json={
            "first_name": "Owner", "last_name": "Test",
            "email": unique_email
        })
        print(user_res.get_json())
        self.owner_id = user_res.get_json().get('id')

        if 'id' not in user_res.get_json():
            a = "Failed to create user in setUp: "
            raise Exception(f"{a}{user_res.get_json()}")

        self.owner_id = user_res.get_json()['id']

    def test_place_immutability_and_validation(self):

        place_data = {
            "title": "Nice Apartment",
            "description": "A very nice place",
            "price": 50.0,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": self.owner_id,
            "amenities": []
        }
        create_res = self.client.post('/api/v1/places/', json=place_data)
        self.assertEqual(create_res.status_code, 201)
        place_id = create_res.get_json()['id']

        update_res = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "Updated Title",
            "latitude": 10.0
        })
        self.assertEqual(update_res.status_code, 200)

        get_res = self.client.get(f'/api/v1/places/{place_id}')
        updated_data = get_res.get_json()
        self.assertEqual(updated_data['title'], "Updated Title")
        self.assertEqual(updated_data['latitude'], 48.8566)

    def test_place_update_invalid_price(self):

        unique_title = f"Test Place {uuid.uuid4().hex[:6]}"
        payload = {
            "title": unique_title,
            "description": "Description de test",
            "price": 100.0,
            "latitude": 45.0,
            "longitude": 1.0,
            "owner_id": self.owner_id,
            "amenities": []
        }
        create_res = self.client.post('/api/v1/places/', json=payload)

        data = create_res.get_json()
        self.assertEqual(create_res.status_code, 201, f"Erreur creation: {data}")

        place_id = data['id']

        update_res = self.client.put(f'/api/v1/places/{place_id}', json={"price": -10.0})
        self.assertEqual(update_res.status_code, 400)

    def test_place_amenities_relation(self):

        amenity_res = self.client.post('/api/v1/amenities/',
                                       json={"name": "WiFi"})
        amenity_id = amenity_res.get_json()['id']

        place_data = {
            "title": "Connected Condo",
            "description": "Fast internet",
            "price": 100.0,
            "latitude": 40.0,
            "longitude": -70.0,
            "owner_id": self.owner_id,
            "amenities": [amenity_id]
        }
        response = self.client.post('/api/v1/places/', json=place_data)
        self.assertEqual(response.status_code, 201)

        place_id = response.get_json()['id']
        get_res = self.client.get(f'/api/v1/places/{place_id}')
        self.assertIn(amenity_id, get_res.get_json()['amenities'])

    def test_place_invalid_coordinates(self):

        res_lat = self.client.post('/api/v1/places/', json={
            "title": "Sky",
            "price": 10, "latitude": 150,
            "longitude": 0,
            "owner_id": self.owner_id
        })
        self.assertEqual(res_lat.status_code, 400)

        res_long = self.client.post('/api/v1/places/', json={
            "title": "Abyss",
            "price": 10,
            "latitude": 0,
            "longitude": -200,
            "owner_id": self.owner_id
        })
        self.assertEqual(res_long.status_code, 400)

    def test_get_non_existent_place(self):
        response = self.client.get('/api/v1/places/999-inconnu')
        self.assertEqual(response.status_code, 404)

    def test_update_non_existent_place(self):
        response = self.client.put('/api/v1/places/999-inconnu',
                                   json={"title": "Ghost Place"})
        self.assertEqual(response.status_code, 404)
