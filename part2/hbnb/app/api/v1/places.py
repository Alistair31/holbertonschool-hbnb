from app.services import facade


@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        # 1. On vérifie d'abord si la place existe
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')

        # 2. On récupère les reviews liées à cette place via la façade
        reviews = facade.get_reviews_by_place(place_id)
        
        # 3. On formate la réponse
        return [{
            'id': r.id,
            'text': r.text,
            'rating': r.rating,
            'user_id': r.user_id
        } for r in reviews], 200
