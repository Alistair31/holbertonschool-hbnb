from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})


@api.route('/')
class UserList(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)
    def post(self):
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        """Register a new user"""
        user_data = api.payload

        try:
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201
        except ValueError as e:
            # Capture "invalid email format" ou "Email already exists"
            api.abort(400, str(e))
        except TypeError as e:
            # Capture "Must be a string type entry"
            api.abort(400, str(e))

    @jwt_required()
    @api.response(200, 'Users retrieved successfully')
    @api.response(404, 'No users found')
    def get(self):
        """Get all users"""
        users = facade.get_users()
        if not users:
            return {'error': 'No users found'}, 404
        return [{'id': user.id, 'first_name': user.first_name,
                 'last_name': user.last_name, 'email': user.email}
                for user in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name,
                'last_name': user.last_name, 'email': user.email}, 200

    @jwt_required()
    @api.expect(user_model, validate=True)
    def put(self, user_id):
        """Update user details (Admin bypass)"""
        claims = get_jwt()
        current_user_id = get_jwt_identity()
        is_admin = claims.get('is_admin', False)

        if not is_admin and str(current_user_id) != str(user_id):
            api.abort(403, "Unauthorized action")

        user_data = api.payload

        if not is_admin and ('email' in user_data or 'password' in user_data):
            api.abort(400, "Regular users cannot modify email or password")

        email = user_data.get('email')
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and str(existing_user.id) != str(user_id):
                api.abort(400, "Email already in use")

        updated_user = facade.update_user(user_id, user_data)
        if not updated_user:
            return {'error': 'User not found'}, 404

        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200

    @jwt_required()
    def delete(self, user_id):
        """Delete a user (Admin bypass)"""
        claims = get_jwt()
        current_user_id = get_jwt_identity()
        is_admin = claims.get('is_admin', False)

        if not is_admin and str(current_user_id) != str(user_id):
            api.abort(403, "Unauthorized action")

        if not facade.get_user_by_id(user_id):
            return {'error': 'User not found'}, 404

        facade.delete_user(user_id)
        return '', 204
