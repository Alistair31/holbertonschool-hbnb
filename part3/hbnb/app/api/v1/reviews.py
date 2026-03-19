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
    @api.response(401, 'Token is missing or invalid')
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
        if any(str(r.user.id if hasattr(r.user,
                                        'id') else r.user_id) == str(
                                            current_user_id
                                            ) for r in existing_reviews):
            api.abort(400, "You have already reviewed this place")

        review_data['user_id'] = current_user_id

        try:
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user.id if hasattr(
                    new_review.user, 'id') else new_review.user_id,
                'place_id': new_review.place.id if hasattr(
                    new_review.place, 'id') else new_review.place_id
            }, 201
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [{
            'id': r.id,
            'text': r.text,
            'rating': r.rating,
            'user_id': r.user.id if hasattr(r.user, 'id') else r.user_id,
            'place_id': r.place.id if hasattr(r.place, 'id') else r.place_id
        } for r in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
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
    @api.expect(review_update_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    def put(self, review_id):
        """Update a review's information"""
        claims = get_jwt()
        current_user_id = get_jwt_identity()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')

        author_id = review.user.id if hasattr(review.user, 'id'
                                              ) else review.user_id

        if not is_admin and str(author_id) != str(current_user_id):
            return {'error': 'Unauthorized action'}, 403

        review_data = api.payload
        try:
            updated_review = facade.update_review(review_id, review_data)
            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'user_id': author_id,
                'place_id': updated_review.place.id if hasattr(
                    updated_review.place, 'id') else updated_review.place_id
            }, 200
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

    @jwt_required()
    @api.response(204, 'Review deleted successfully')
    @api.response(403, 'Unauthorized action')
    def delete(self, review_id):
        """Delete a review (Author or Admin)"""
        claims = get_jwt()
        current_user_id = get_jwt_identity()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if not is_admin and str(review.user.id if hasattr(
                review.user,
                'id') else review.user_id) != str(current_user_id):
            return {'error': 'Unauthorized action'}, 403

        facade.delete_review(review_id)
        return '', 204


@api.route('/places/<place_id>')
class PlaceReviewList(Resource):
    @api.response(200, 'Reviews for the place retrieved successfully')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)

        return [{
            'id': r.id,
            'text': r.text,
            'rating': r.rating,
            'user_id': r.user_id,
            'place_id': r.place_id
        } for r in reviews], 200
