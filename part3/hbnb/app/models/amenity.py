from app.models.base_models import BaseModel
from app import db


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(10), nullable=True, default='🏠')
    icon_url = db.Column(db.String(255), nullable=True)

    def __init__(self, name: str, icon: str = '🏠', **kwargs):

        super().__init__(**kwargs)

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")

        self.name = name
        self.icon = icon

    @staticmethod
    def verification_name(name: str) -> bool:
        """Vérifie si name est une chaîne de caractères non vide."""
        return isinstance(name, str) and bool(name.strip())
