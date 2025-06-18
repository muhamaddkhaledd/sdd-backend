from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
from loginsignup.auth.models import User
from loginsignup.auth.utils import authenticate_user
from datetime import datetime


class Register(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', required=True, help="First name cannot be blank!")
        parser.add_argument('last_name', required=True, help="Last name cannot be blank!")
        parser.add_argument('email', required=True, help="Email cannot be blank!")
        parser.add_argument('password', required=True, help="Password cannot be blank!")
        parser.add_argument('birthdate', required=True, help="Birthdate cannot be blank!")
        parser.add_argument('profile_image', type=FileStorage, location='files')

        args = parser.parse_args()

        if User.find_by_email(args['email']):
            return {'message': 'User already exists'}, 400

        try:
            user_id = User.create_user(
                first_name=args['first_name'],
                last_name=args['last_name'],
                email=args['email'],
                password=args['password'],
                birthdate=args['birthdate'],
                profile_image=args['profile_image']
            )
            return {'message': 'User created successfully', 'user_id': user_id}, 201
        except ValueError as e:
            return {'message': str(e)}, 400

class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, help="Email cannot be blank!")
        parser.add_argument('password', required=True, help="Password cannot be blank!")
        args = parser.parse_args()

        return authenticate_user(args['email'], args['password'])

def initialize_routes(api):
    api.add_resource(Register, '/register')
    api.add_resource(Login, '/login')