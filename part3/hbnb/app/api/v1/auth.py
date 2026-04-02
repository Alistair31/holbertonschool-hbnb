from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity


api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""

        from app.services import facade
        credentials = api.payload
        # Get the email and password from the request payload

        # Step 1: Retrieve the user based on the provided email
        user = facade.get_user_by_email(credentials['email'])
        # Step 2: Check if the user exists and the password is correct
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Step 3: Create a JWT token with the user's id and is_admin flag
        access_token = create_access_token(identity=str(user.id),
                                           additional_claims={"is_admin":
                                                              user.is_admin})
        # Step 4: Return the JWT token to the client
        return {'access_token': access_token}, 200


register_model = api.model('Register', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/register')
class Register(Resource):
    @api.expect(register_model)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or invalid data')
    def post(self):
        """Register a new user (public)"""
        from app.services import facade
        data = api.payload
        try:
            new_user = facade.create_user(data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        print("jwt------")
        print(get_jwt_identity())
        current_user = get_jwt_identity()
        # if you need to see if the user is an admin or not,
        # you can access additional claims using get_jwt() :
        # addtional claims = get_jwt()
        # additional claims["is_admin"] -> True or False
        return {'message': f'Hello, user {current_user}'}, 200
