import unittest
from app import create_app, db
from app.services import facade
from app.models.place import Place

class TestRelations(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            
            # 1. Création des objets
            user = facade.create_user({
                "first_name": "Owner", "last_name": "Test", 
                "email": "owner@test.com", "password": "password"
            })
            place = facade.create_place({
                "title": "House", "price": 100.0, "latitude": 0.0, 
                "longitude": 0.0, "owner_id": user.id, "description": "Nice"
            })
            
            # 2. ON STOCKE LES IDS (Simples strings)
            # Ne stocke pas l'objet entier (self.p = place), sinon il devient "Detached"
            self.user_id = user.id
            self.place_id = place.id

    def test_place_owner_relation(self):
        """Vérifie que la place appartient bien à l'utilisateur (Task 8)"""
        with self.app.app_context():
            # On récupère l'objet frais via l'ID stocké
            place_in_db = db.session.get(Place, self.place_id)
            
            self.assertIsNotNone(place_in_db)
            # Test de la clé étrangère
            self.assertEqual(place_in_db.owner_id, self.user_id)
            # Test de la relation (backref)
            self.assertEqual(place_in_db.owner.email, "owner@test.com")
