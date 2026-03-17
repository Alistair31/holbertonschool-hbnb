
from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review
from app.models.place import Place


class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    def create_user(self, user_data):
        existing_user = self.user_repo.get_by_attribute('email',
                                                        user_data['email'])
        if existing_user:
            raise ValueError("Email already registered")
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user_by_id(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None

        self.user_repo.update(user_id, user_data)

        return user

    def delete_user(self, user_id):
        user = self.user_repo.get(user_id)
        if not user:
            return False

        self.user_repo.delete(user_id)
        return True

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
        return self.amenity_repo.get_by_attribute('name', name)

    def delete_amenity(self, amenity_id):
        # logic to delete an amenity
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return False

        self.amenity_repo.delete(amenity_id)
        return True

    def create_place(self, place_data):
        from app.models.place import Place

        owner_id = place_data.pop('owner_id', None)
        amenity_ids = place_data.pop('amenities', [])

        place_data['owner_id'] = owner_id

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
        return self.place_repo.get_by_attribute('title', title)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None

        place_data.pop('latitude', None)
        place_data.pop('longitude', None)

        if 'amenities' in place_data:
            amenity_ids = place_data.pop('amenities')
            place.amenities = []
            for a_id in amenity_ids:
                amenity = self.get_amenity(a_id)
                if amenity:
                    place.add_amenity(amenity)
        for key, value in place_data.items():
            if hasattr(place, key):
                setattr(place, key, value)
        place.validate()
        self.place_repo.update(place_id, place_data)

        return place

    def delete_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            return False

        self.place_repo.delete(place_id)
        return True

    def create_review(self, review_data):
        from app.models.review import Review

        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')

        user_obj = self.get_user_by_id(user_id)
        place_obj = self.get_place(place_id)

        if not user_obj:
            raise ValueError("User not found")
        if not place_obj:
            raise ValueError("Place not found")
        current_owner_id = place_obj.owner_id
        if current_owner_id == user_obj.id:
            raise ValueError("You cannot review your own place!")

        review_params = {
            "text": review_data.get('text'),
            "rating": review_data.get('rating'),
            "user_id": user_obj,
            "place_id": place_obj
        }

        new_review = Review(**review_params)

        self.review_repo.add(new_review)
        return new_review

    def get_review(self, review_id):
        # logic to retrieve a review by ID
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        # logic to retrieve all reviews
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return [r for r in self.get_all_reviews() if r.place_id == place_id]

    def update_review(self, review_id, review_data):
        # logic to update a review
        self.review_repo.update(review_id, review_data)
        return self.get_review(review_id)

    def delete_review(self, review_id):
        # logic to delete a review
        self.review_repo.delete(review_id)
