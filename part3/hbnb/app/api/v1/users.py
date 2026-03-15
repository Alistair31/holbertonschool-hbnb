from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required


api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True,
                                description='First name of the user'),
    'last_name': fields.String(required=True,
                               description='Last name of the user'),
    'email': fields.String(required=True,
                           description='Email of the user'),
    'password': fields.String(required=True,
                              description='Password of the user')
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    def post(self):
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

    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user details"""
        user_data = api.payload
        user = facade.get_user_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        updated_user = facade.update_user(user_id, user_data)
        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200

    @api.response(204, 'User successfully deleted')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user by ID"""
        user = facade.get_user_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        facade.delete_user(user_id)
        return '', 204
