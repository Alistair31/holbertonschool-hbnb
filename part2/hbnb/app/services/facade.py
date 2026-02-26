from app.persistence.repository import InMemoryRepository
from app.models.user import User


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None

        self.user_repo.update(user_id, user_data)

        return user

    def create_amenity(self, amenity_data):
        # logic to create an amenity
        from app.models.amenity import Amenity
        new_amenity = Amenity(**amenity_data)
        self.amenity_repo.add(new_amenity)
        return new_amenity

    def get_amenity(self, amenity_id):
        # logic to retrieve an amenity by ID
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        # logic to retrieve all amenities
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        # logic to update an amenity
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.amenity_repo.get(amenity_id)

    def get_amenity_by_name(self, name):
        # logic to retrieve an amenity by name
        all_amenities = self.amenity_repo.get_all()
        return next((a for a in all_amenities if a.name == name), None)

    def create_place(self, place_data):
        from app.models.place import Place

        owner_id = place_data.pop('owner_id', None)
        amenity_ids = place_data.pop('amenities', [])

        place_data['owner'] = owner_id

        new_place = Place(**place_data)

        for a_id in amenity_ids:
            amenity = self.get_amenity(a_id)
            if amenity:
                new_place.add_amenity(amenity)

        self.place_repo.add(new_place)
        return new_place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_place_by_title(self, title):
        all_places = self.place_repo.get_all()
        return next((p for p in all_places if p.title == title), None)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        self.place_repo.update(place_id, place_data)
        return self.place_repo.get(place_id)

    def create_review(self, review_data):
        # logic to create a review
        from app.models.review import Review

        if not self.get_place(review_data.get('place_id')):
            raise ValueError("Place not found")

        if not self.get_user(review_data.get('user_id')):
            raise ValueError("User not found")

        new_review = Review(**review_data)
        self.review_repo.add(new_review)
        return new_review

    def get_review(self, review_id):
        # logic to retrieve a review by ID
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        # logic to retrieve all reviews
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        # logic to retrieve all reviews for a specific place
        all_reviews = self.get_all_reviews()
        return [review for review in all_reviews
                if review.place_id == place_id]

    def update_review(self, review_id, review_data):
        # logic to update a review
        self.review_repo.update(review_id, review_data)
        return self.get_review(review_id)

    def delete_review(self, review_id):
        # logic to delete a review
        self.review_repo.delete(review_id)
