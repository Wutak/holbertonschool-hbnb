from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='password of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400
        
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of users"""
        users = facade.get_users()
        return [user.to_dict() for user in users], 200
    
@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @api.expect(user_model)
    @jwt_required()
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(403, 'Unauthorized action')
    @api.response(403, "Unauthorized action, you cannot change this user's informations")
    @api.response(403, 'You cannot modify id')
    @api.response(400, 'You canot modify email or password.')
    def put(self, user_id):
        from app import bcrypt

        user_data = api.payload
        user = facade.get_user(user_id)
        user_id = get_jwt_identity()['id']
        user_id_from_token = get_jwt_identity().get("id")

        # User is authenticated
        if user_id_from_token != user.id:
            return {"error": "Unauthorized action"}, 403

        # Can't modify other's informations
        if user_id != user.id:
            return {"error": "Unauthorized action, you cannot change this user's informations"}, 403

        if "user_id" in user_data:
            return {'You cannot modify id'}, 403

        if user.email != user_data["email"]:
            return {"error": "You cannot modify email or password."}, 400
        else:
            user_data.pop("email")

        if not user:
            return {'error': 'User not found'}, 404
        try:
            facade.update_user(user_id, user_data)
            return user.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        email = user_data.get('email')

        # Check if email is already in use
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        facade.create_user(user_data)
        return {'message': 'User created successfully'}, 201

@api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')

        # Ensure email uniqueness
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400
        facade.update_user(user_id, data)
        return {'message': 'User updated successfully'}, 200
