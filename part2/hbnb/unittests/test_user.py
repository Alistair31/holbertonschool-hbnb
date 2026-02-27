import unittest
import uuid
from app import create_app


class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user_success(self):
        unique_email = f"user_{uuid.uuid4().hex[:6]}@test.com"
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": unique_email
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.get_json())

    def test_create_user_duplicate_email(self):
        email = "duplicate@test.com"
        self.client.post('/api/v1/users/', json={
            "first_name": "User1", "last_name": "Test", "email": email
        })
        response = self.client.post('/api/v1/users/', json={
            "first_name": "User2", "last_name": "Test", "email": email
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("exists", response.get_json().get('message', '').lower())

    def test_create_user_missing_fields(self):
        response = self.client.post('/api/v1/users/', json={
            "last_name": "Doe", "email": "missing@test.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_user_by_id(self):
        res = self.client.post('/api/v1/users/', json={
            "first_name": "Fetch", "last_name": "Me", "email": "fetch@test.com"
        })
        user_id = res.get_json()['id']

        get_res = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.get_json()['first_name'], "Fetch")

    def test_get_non_existent_user(self):
        response = self.client.get('/api/v1/users/non-existent-id')
        self.assertEqual(response.status_code, 404)

    def test_update_user(self):
        res = self.client.post('/api/v1/users/', json={
            "first_name": "Old", "last_name": "Name", "email": "update@test.com"
        })
        user_id = res.get_json()['id']

        update_res = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "New",
            "last_name": "Name",
            "email": "update@test.com"
        })
        self.assertEqual(update_res.status_code, 200)
