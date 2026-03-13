from flask_jwt_extended import get_jwt, jwt_required
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload

        existing_amenity = facade.get_amenity_by_name(amenity_data.get('name'))
        if existing_amenity:
            return {'error': 'Amenity already registered'}, 400
        if not isinstance(amenity_data.get('name'), str):
            return {'error': 'Amenity name must be a string'}, 400
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return {'id': new_amenity.id, 'name': new_amenity.name}, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [{'id': amenity.id, 'name': amenity.name}
                for amenity in amenities], 200

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [{'id': amenity.id, 'name': amenity.name}
                for amenity in amenities], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update amenity details"""
        amenity_data = api.payload
        if not isinstance(amenity_data.get('name'), str):
            return {'error': 'Amenity name must be a string'}, 400
        if not amenity_data.get('name', '').strip():
            return {'error': 'Amenity name cannot be empty'}, 400
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        if not updated_amenity:
            return {'error': 'Amenity not found'}, 404

        return {
            'message': 'Amenity updated successfully',
            'id': updated_amenity.id,
            'name': updated_amenity.name
        }, 200

    @api.route('/amenities/<amenity_id>')
    class AdminAmenityModify(Resource):
        @jwt_required()
        def put(self, amenity_id):
            current_user = get_jwt()
            if not current_user.get('is_admin'):
                return {'error': 'Admin privileges required'}, 403

            # Logic to update an amenity
            pass


@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        # Logic to create a new amenity
        pass
