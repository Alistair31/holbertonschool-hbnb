from flask_jwt_extended import get_jwt, jwt_required
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True,
                           description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True,
                          description='Price per night'),
    'latitude': fields.Float(required=True,
                             description='Latitude of the place'),
    'longitude': fields.Float(required=True,
                              description='Longitude of the place'),
    'owner_id': fields.String(required=True,
                              description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True,
                             description="List of amenities ID's")
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload

        try:
            new_place = facade.create_place(place_data)

            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner.id
                if hasattr(new_place.owner, 'id') else new_place.owner,
                'amenities': [a.id for a in new_place.amenities]
            }, 201

        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [{'id': place.id, 'title': place.title,
                 'description': place.description, 'price': place.price,
                 'latitude': place.latitude, 'longitude': place.longitude,
                 'owner_id': place.owner.id
                 if hasattr(place.owner, 'id') else place.owner,
                 'amenities': [a.id for a in place.amenities]}
                for place in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {'id': place.id, 'title': place.title,
                'description': place.description, 'price': place.price,
                'latitude': place.latitude, 'longitude': place.longitude,
                'owner_id': place.owner.id
                if hasattr(place.owner, 'id') else place.owner,
                'amenities': [a.id for a in place.amenities]}, 200

    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        try:

            place_data = api.payload

            updated_place = facade.update_place(place_id, place_data)

            if not updated_place:
                api.abort(404, "Place not found")
            if updated_place.title is not None:
                if not isinstance(updated_place.title,
                                  str) or updated_place.title.strip() == "":
                    api.abort(400, "Title must be a string")
            if updated_place.description is not None:
                if not isinstance(updated_place.description,
                                  str) or updated_place.description.strip(
                                  ) == "":
                    api.abort(400, "Description must be a string")

            return {
                'id': updated_place.id,
                'title': updated_place.title,
                'description': updated_place.description,
                'price': updated_place.price,
                'owner_id': updated_place.owner.id
                if hasattr(updated_place.owner, 'id') else updated_place.owner,
                'amenities': [a.id if hasattr(a, 'id')
                              else a for a in updated_place.amenities]
            }, 200

        except (ValueError, TypeError) as e:
            api.abort(400, str(e))


@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @jwt_required()
    def put(self, place_id):
        current_user = get_jwt()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        # Logic to update the place
        pass
