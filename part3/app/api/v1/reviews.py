from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Place not found')
    @api.response(400, 'User not found')
    @api.response(403, 'Unauthorized action, you must be logged in to review a place')
    @api.response(400, 'User cannot review their own place')
    @api.response(400, 'Unauthorized action, you have already reviewed this place')
    def post(self):
        """Register a new review"""
        review_data = api.payload
        current_user = get_jwt_identity()

        # User exists
        user = facade.get_user(review_data['user_id'])
        if not user:
            return {'error': 'User not found'}, 400
        # Place exists
        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 400
        # User authenticated
        if review_data['user_id'] != current_user:
            return {'error': 'Unauthorized action, you must be logged in to review a place'}, 403
        # No multiple reviews
        reviews = facade.get_reviews_by_place(review_data['place_id'])
        if reviews != []:
            for review in reviews:
                if review['user_id'] == current_user:
                    return {'error': 'Unauthorized action, you have already reviewed this place'}, 400
        var_place = facade.get_place(review_data['place_id'])
        var_user = facade.get_user(review_data['user_id'])
        owner_id = var_place.owner_id
        owner_id_in_review_data = review_data['user_id']

        # No selfreviews
        if place.owner.id == user.id:
            return {'error': 'User cannot review their own place'}, 400

        try:
            new_review = facade.create_review(review_data)
            return new_review.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        return [review.to_dict() for review in facade.get_all_reviews()], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @api.expect(review_model)
    @jwt_required()
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        review_data = api.payload
        review = facade.get_review(review_id)
        # User authenticated
        if review_data['user_id'] != current_user:
            return {'error': 'Unauthorized action, you must be logged in to update a review'}, 403

        # Only update own reviews
        if user_id != review.id:
            return {'error': 'Unauthorized action, you cannot update this review'}, 403

        if not review:
            return {'error': 'Review not found'}, 404
        
        try:
            facade.update_review(review_id, review_data)
            return {'message': 'Review updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        review = facade.get_review(review_id)
        # User authenticated
        if review_data['user_id'] != current_user:
            return {'error': 'Unauthorized action, you must be logged in to delete a place'}, 403

        # Only delete own reviews
        if user_id != review.id:
            return {'error': 'Unauthorized action, you cannot delete this review'}, 403

        if not review:
            return {'error': 'Review not found'}, 404
        
        try:
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400
