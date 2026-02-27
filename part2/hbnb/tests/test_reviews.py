import unittest
from app import create_app

class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        import uuid
        unique_email = f"test_{uuid.uuid4()}@hbnb.com"

        # 1. Créer l'utilisateur
        user_res = self.client.post('/api/v1/users/', json={
            "first_name": "Test", 
            "last_name": "User", 
            "email": unique_email
        })
        self.user_id = user_res.get_json().get('id')

        # 2. Créer la Place
        place_res = self.client.post('/api/v1/places/', json={
            "title": "Test House",
            "description": "A nice place to test",
            "price": 100.0,
            "latitude": 34.0,
            "longitude": -118.0,
            "owner_id": self.user_id
        })
        self.place_id = place_res.get_json().get('id')

        # Sécurité : Si l'un des deux a échoué, on affiche l'erreur pour débugger
        if not self.user_id or not self.place_id:
            print(f"DEBUG: User ID: {self.user_id}, Place ID: {self.place_id}")
            print(f"DEBUG: Place Response: {place_res.get_json()}")
            raise Exception("Setup failed: Could not create user or place.")

    def test_create_review_flow(self):
        """Test du cycle complet : Création, Récupération, Update"""

        # --- TEST POST (Création) ---
        review_data = {
            "text": "Super séjour !",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        }
        response = self.client.post('/api/v1/reviews/', json=review_data)
        self.assertEqual(response.status_code, 201)
        review_id = response.get_json()['id']

        # --- TEST GET (Récupération) ---
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['text'], "Super séjour !")

        # --- TEST PUT (Mise à jour) ---
        update_data = {"text": "Séjour correct", "rating": 3}
        response = self.client.put(f'/api/v1/reviews/{review_id}', json=update_data)
        self.assertEqual(response.status_code, 200)

        # --- TEST DELETE (Suppression) ---
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)

    def test_create_review_invalid_rating(self):
        """Test négatif : Le rating doit être entre 1 et 5"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Mauvais rating",
            "rating": 10,  # Note: Ce rating est invalide
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_missing_data(self):
        """Test negative scenario: Missing required fields"""
        response = self.client.post('/api/v1/reviews/', json={
            "rating": 5,
            "user_id": self.user_id
            # Missing text and place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_get_non_existent_review(self):
        """Test retrieving a review that doesn't exist"""
        response = self.client.get('/api/v1/reviews/invalid-id-123')
        self.assertEqual(response.status_code, 404)
