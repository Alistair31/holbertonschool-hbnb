from app.models.base_models import BaseModel
from app import db


class PlaceImage(BaseModel):
    __tablename__ = 'place_images'

    place_id = db.Column(
        db.String(36), db.ForeignKey('places.id'), nullable=False
    )
    image_url = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)

    def __init__(self, place_id, image_url, is_primary=False, **kwargs):
        super().__init__(**kwargs)
        self.place_id = place_id
        self.image_url = image_url
        self.is_primary = is_primary
