from app.models.base_models import BaseModel
import validators
import json


class User(BaseModel):
    def __init__(self, first_name: str, last_name: str,
                 email: str, password=None, is_admin=False):
        super().__init__()

        if isinstance(first_name, str) is False:
            raise TypeError("Must be a string type entry.")
        if isinstance(last_name, str) is False:
            raise TypeError("Must be a string type entry.")
        if isinstance(email, str) is False:
            raise TypeError("Must be a string type entry.")
        if password is not None and isinstance(password, str) is False:
            raise TypeError("Must be a string type entry.")
        if len(first_name) > 50 or len(last_name) > 50:
            raise ValueError("Oversized text, must be 50 character max.")
        if isinstance(is_admin, bool) is False:
            raise TypeError("Must be True or False")

        self.first_name: str = first_name
        self.last_name: str = last_name
        self.email: str = email
        self.password: str = password
        self.is_admin: bool = is_admin

    @staticmethod
    def is_valid_email(email):
        return validators.email(email) is not None

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
