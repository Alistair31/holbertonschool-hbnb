from unitests.base_test import BaseTestCase
from app.services import facade
from app.models.place import Place
from app import db

class TestPlaceRelations(BaseTestCase):
    def test_place_integrity_and_ownership(self):
        """Validate the link between a Place and its Owner in the database."""
        # Setup data
        user = facade.create_user({"first_name": "Host", "last_name": "X", 
                                   "email": "host@hbnb.io", "password": "pwd"})
        place = facade.create_place({
            "title": "Luxury Villa", "price": 250.0, "latitude": 48.8, 
            "longitude": 2.3, "owner_id": user.id, "description": "Beautiful view"
        })

        # Test
        place_in_db = db.session.get(Place, place.id)
        self.assertIsNotNone(place_in_db, "Place should exist in DB")
        self.assertEqual(place_in_db.owner.email, "host@hbnb.io", "Relationship should resolve to the correct owner")
        self.assertEqual(len(user.places), 1, "User's back-reference should show 1 place owned")
