from app.models.base_models import BaseModel
from app import db
import validators


class User(BaseModel, db.Model):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship('Place', back_populates='owner',
                             cascade="all, delete-orphan")
    reviews = db.relationship('Review', back_populates='user', lazy=True)

    def __init__(self, first_name: str, last_name: str,
                 email: str, password=None, is_admin=False):
        super().__init__()

        if not isinstance(first_name, str):
            raise TypeError("Must be a string type entry.")
        if len(first_name) == 0:
            raise ValueError("First name cannot be empty.")
        if not isinstance(last_name, str):
            raise TypeError("Must be a string type entry.")
        if len(last_name) == 0:
            raise ValueError("Last name cannot be empty.")
        if not isinstance(email, str):
            raise TypeError("Must be a string type entry.")
        if not self.is_valid_email(email):
            raise ValueError("invalid email format.")
        if not isinstance(password, str):
            raise TypeError("Must be a string type entry.")
        if len(first_name) > 50 or len(last_name) > 50:
            raise ValueError("Oversized text, must be 50 character max.")
        if isinstance(is_admin, bool) is False:
            raise TypeError("Must be True or False")

        self.first_name: str = first_name
        self.last_name: str = last_name
        self.email: str = email
        self.is_admin: bool = is_admin
        if password:
            self.hash_password(password)

    @staticmethod
    def is_valid_email(email):
        return validators.email(email) is True

    def hash_password(self, password):
        from app import bcrypt
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        from app import bcrypt
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
