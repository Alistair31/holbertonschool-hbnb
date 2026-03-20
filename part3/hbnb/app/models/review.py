from app.models.base_models import BaseModel
from app import db


class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, text: str, rating: int, place_id, user_id, **kwargs):
        super().__init__(**kwargs)


        p_id = place_id.id if hasattr(place_id, 'id') else place_id
        u_id = user_id.id if hasattr(user_id, 'id') else user_id

        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        self.text = text
        self.rating = rating
        self.place_id = p_id
        self.user_id = u_id
