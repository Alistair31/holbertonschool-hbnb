import unittest
from app import create_app

class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        """Configuration initiale avant chaque test"""
        self.app = create_app()
        self.client = self.app.test_client()
        
        # 1. On crée d'abord un User pour avoir un ID valide
        user_res = self.client.post('/api/v1/users/', json={
            "first_name": "Test", "last_name": "User", "email": "test@hbnb.com"
        })
        self.user_id = user_res.get_json()['id']

        # 2. On crée une Place (liée à cet User)
        # Note: Assure-toi que la route /places/ est fonctionnelle chez ton collègue
        place_res = self.client.post('/api/v1/places/', json={
            "title": "Apartment", "description": "Nice place", 
            "price": 100, "latitude": 48.8, "longitude": 2.3, "owner_id": self.user_id
        })
        self.place_id = place_res.get_json()['id']

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
