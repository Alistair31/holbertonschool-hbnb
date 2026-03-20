from app.models.base_models import BaseModel
from app import db

class Amenity(BaseModel):
    __tablename__ = 'amenities'


    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name: str, **kwargs):

        super().__init__(**kwargs)


        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")

        self.name = name

    @staticmethod
    def verification_name(name: str) -> bool:
        """Vérifie si name est une chaîne de caractères non vide."""
        return isinstance(name, str) and bool(name.strip())
