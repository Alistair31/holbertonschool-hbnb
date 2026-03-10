from app.models.base_models import BaseModel
import validators
import json
from app import bcrypt


class User(BaseModel):
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
        # if not isinstance(password, str):
            # raise TypeError("Must be a string type entry.")
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
        else:
            self.password = None

    @staticmethod
    def is_valid_email(email):
        return validators.email(email) is True

    @staticmethod
    def is_email_unique(db_path, email):
        try:
            with open(db_path, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return True
        for user in data:
            if user.get("email") == email:
                return False
        return True

    @staticmethod
    def validate_and_check_unique(email, db_path):
        if not User.is_valid_email(email):
            return False, "Wrong format for email address"
        return User.is_email_unique(db_path, email), "Email ok"

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None

        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        if hasattr(user, 'validate'):
            user.validate()

        self.user_repo.update(user_id, user_data)

        return user

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
