from app.models.base_models import BaseModel


class Place(BaseModel):
    def __init__(self, title: str, description: str, price: float,
                 latitude: float, longitude: float, owner: str):
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
        if not isinstance(owner, str):
            raise ValueError("Owner must be a string")
        if len(owner) == 0:
            raise ValueError("Owner cannot be empty")

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
