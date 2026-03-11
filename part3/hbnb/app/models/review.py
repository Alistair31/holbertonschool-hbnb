from app.models.base_models import BaseModel
from app.models.place import Place
from app.models.user import User


class Review(BaseModel):
    def __init__(self, text: str, rating: int, place_id: Place, user_id: User):
        super().__init__()

        if not isinstance(place_id, Place):
            raise ValueError("Place must be an instance of Place")
        if not self.verification_place(place_id):
            raise ValueError("Place does not exist")
        if not isinstance(user_id, User):
            raise ValueError("User must be an instance of User")
        if not self.verification_user(user_id):
            raise ValueError("User does not exist")
        if not isinstance(rating, int):
            raise ValueError("Rating must be an integer")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        if not isinstance(text, str):
            raise ValueError("Text must be a string")
        if not text:
            raise ValueError("Text cannot be empty")

        self.text: str = text
        self.rating: int = rating
        self.place: Place = place_id
        self.user: User = user_id

    @staticmethod
    def verification_place(place: Place | None) -> bool:
        """Vérifie si place existe."""
        return place is not None

    @staticmethod
    def verification_user(user: User | None) -> bool:
        """Vérifie si user existe."""
        return user is not None
