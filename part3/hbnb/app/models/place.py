from app.models.base_models import BaseModel
from app.models.user import User
from app import db

place_amenities = db.Table('place_amenity',
                           db.Column('place_id', db.String(36),
                                     db.ForeignKey('places.id'),
                                     primary_key=True),
                           db.Column('amenity_id', db.String(36),
                                     db.ForeignKey('amenities.id'),
                                     primary_key=True)
                           )


class Place(BaseModel, db.Model):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'),
                         nullable=False)

    owner = db.relationship('User', back_populates='places')
    reviews = db.relationship('Review', back_populates='place',
                              cascade="all, delete-orphan")
    amenities = db.relationship('Amenity', secondary='place_amenity',
                                back_populates='places')

    def __init__(self, title: str, description: str, price: float,
                 latitude: float, longitude: float, owner: User):
        super().__init__()

        if not isinstance(title, str):
            raise ValueError("Title must be a string")
        if len(title) == 0:
            raise ValueError("Title cannot be empty")
        if not isinstance(description, str):
            raise ValueError("Description must be a string")
        if len(description) == 0:
            raise ValueError("Description cannot be empty")
        if not isinstance(price, (int, float)):
            raise ValueError("Price must be a number")
        if price <= 0:
            raise ValueError("Price must be a positive number")
        if not isinstance(latitude, (int, float)):
            raise ValueError("Latitude must be a number")
        if latitude < -90 or latitude > 90:
            raise ValueError("Latitude must be between -90 and 90")
        if not isinstance(longitude, (int, float)):
            raise ValueError("Longitude must be a number")
        if longitude < -180 or longitude > 180:
            raise ValueError("Longitude must be between -180 and 180")
        if not isinstance(owner, User):
            raise ValueError("Owner must be a User instance")

        self.title: str = title
        self.description: str = description
        self.price: float = price
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.owner: User = owner

        self.validate()

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def validate(self):
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("Title cannot be empty")
        if self.price <= 0:
            raise ValueError("Price must be a positive number")
        if self.latitude < -90 or self.latitude > 90:
            raise ValueError("Latitude must be between -90 and 90")
        if self.longitude < -180 or self.longitude > 180:
            raise ValueError("Longitude must be between -180 and 180")
        if not self.owner:
            raise ValueError("Owner cannot be empty")
