from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity
api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User',{
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='password of the user')
})

bcrypt = Bcrypt()

@api.route('/')
class UserList(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        print(f"Requête POST reçue avec les données : {user_data}")
        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
             # Hash the password before creating the user
            user_data['password'] = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
            new_user = facade.create_user(user_data)
            print(f"Utilisateur créé : {new_user.to_dict()}")
            return new_user.to_dict(), 201
        except Exception as e:
            print(f"Erreur lors de la création de l'utilisateur : {e}")
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
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        user_data = api.payload
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        try:
            if 'password' in user_data:
                password_hash = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
                user_data['password'] = password_hash
            facade.update_user(user_id, user_data)
            return user.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400
