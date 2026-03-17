from app.models.base_models import BaseModel
from app.models.place import Place
from app.models.user import User
from app import db


class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    place_id = db.Column(db.String(36), db.ForeignKey('places.id'),
                         nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'),
                        nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'place_id', name='unique_user_place_review'),
    )

    place = db.relationship('Place', back_populates='reviews')
    user = db.relationship('User')

    def __init__(self, text: str, rating: int, place_id: Place, user_id: User):
        super().__init__()

        if not text or not isinstance(text, str):
            raise ValueError("Text must be a non-empty string")
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        if not isinstance(place_id, Place):
            raise ValueError("place must be a valid instance of Place")
        if not isinstance(user_id, User):
            raise ValueError("user must be a valid instance of User")

        self.text: str = text
        self.rating: int = rating
        if hasattr(place_id, 'id'):
            self.place_id = place_id.id
        else:
            self.place_id = place_id
        if hasattr(user_id, 'id'):
            self.user_id = user_id.id
        else:
            self.user_id = user_id

    @staticmethod
    def verification_place(place: Place | None) -> bool:
        """Vérifie si place existe."""
        return place is not None

    @staticmethod
    def verification_user(user: User | None) -> bool:
        """Vérifie si user existe."""
        return user is not None
