from app.models.base_models import BaseModel
from app import db

place_amenity = db.Table('place_amenity',
                         db.Column('place_id', db.String(36),
                                   db.ForeignKey('places.id'),
                                   primary_key=True),
                         db.Column('amenity_id', db.String(36),
                                   db.ForeignKey('amenities.id'),
                                   primary_key=True)
                         )


place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)


class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)


    reviews = db.relationship('Review', backref='place', lazy=True, cascade="all, delete-orphan")
    amenities = db.relationship('Amenity', secondary=place_amenity, backref='places')

    def __init__(self, title: str, description: str, price: float,
                 latitude: float, longitude: float, owner_id: str, **kwargs):
        super().__init__(**kwargs)

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        
        self.validate()


    def validate(self):
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("Title cannot be empty")
        if self.price <= 0:
            raise ValueError("Price must be a positive number")
        if self.latitude < -90 or self.latitude > 90:
            raise ValueError("Latitude must be between -90 and 90")
        if self.longitude < -180 or self.longitude > 180:
            raise ValueError("Longitude must be between -180 and 180")
        if not self.owner_id or len(self.owner_id.strip()) == 0:
            raise ValueError("Owner cannot be empty")
