from app.models.base_models import BaseModel


class Place(BaseModel):
    def __init__(self, title: str, description: str, price: float,
                 latitude: float, longitude: float, owner: str):
        super().__init__()
        self.title: str = title
        self.description: str = description
        self.price: float = price
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.owner: str = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
