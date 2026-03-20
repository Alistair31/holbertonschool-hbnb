from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


api = Namespace('reviews', description='Review operations')


review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(description='Updated text of the review'),
    'rating': fields.Integer(description='Updated rating (1-5)')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new review"""
        review_data = api.payload
        current_user_id = get_jwt_identity()
        place_id = review_data.get('place_id')

        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")

        if str(place.owner_id) == str(current_user_id):
            api.abort(400, "You cannot review your own place")

        existing_reviews = facade.get_reviews_by_place(place_id)
        if any(str(r.user_id) == str(current_user_id) for r in existing_reviews):
            api.abort(400, "You have already reviewed this place")

        review_data['user_id'] = current_user_id

        try:
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': current_user_id,
                'place_id': place_id
            }, 201
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [{
            'id': r.id,
            'text': r.text,
            'rating': r.rating,
            'user_id': r.user_id,
            'place_id': r.place_id
        } for r in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id
        }, 200

    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        review = facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')

        if not claims.get('is_admin') and str(review.user_id) != str(current_user_id):
            api.abort(403, "Unauthorized action")

        facade.delete_review(review_id)
        return '', 204
