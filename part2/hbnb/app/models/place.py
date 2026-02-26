from app.models.base_models import BaseModel


class Place(BaseModel):
    def __init__(self, title: str, description: str, price: float,
                 latitude: float, longitude: float, owner: str):
        super().__init__()

        if not isinstance(title, str):
            raise ValueError("Title must be a string")
        if not isinstance(description, str):
            raise ValueError("Description must be a string")
        if not isinstance(price, (int, float)):
            raise ValueError("Price must be a number")
        if not isinstance(latitude, (int, float)):
            raise ValueError("Latitude must be a number")
        if not isinstance(longitude, (int, float)):
            raise ValueError("Longitude must be a number")
        if not isinstance(owner, str):
            raise ValueError("Owner must be a string")

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
