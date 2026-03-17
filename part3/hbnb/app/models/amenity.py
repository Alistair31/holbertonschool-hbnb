from app.models.base_models import BaseModel
from app import db


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(100), nullable=False)
    places = db.relationship('Place', secondary='place_amenity',
                             back_populates='amenities')

    def __init__(self, name: str, description=None):
        super().__init__()

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")

        self.name: str = name

    @staticmethod
    def verification_name(name: str) -> bool:
        """Vérifie si name est une chaîne de caractères non vide."""
        return isinstance(name, str) and bool(name.strip())
