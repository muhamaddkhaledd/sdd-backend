from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import base64
from bson import ObjectId
import json


load_dotenv()

client = MongoClient(os.getenv('MONGO_URI'))
db = client.get_database('auth_db')
users = db.users

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)

class User:
    @staticmethod
    def create_user(first_name, last_name, email, password, birthdate, profile_image=None):
        # Handle image upload
        image_data = None
        if profile_image:
            image_data = base64.b64encode(profile_image.read()).decode('utf-8')

        user_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': generate_password_hash(password).decode('utf-8'),
            'birthdate': datetime.strptime(birthdate, '%Y-%m-%d'),
            'profile_image': image_data,
            'created_at': datetime.utcnow()
        }
        result = users.insert_one(user_data)
        return str(result.inserted_id)

    @staticmethod
    def find_by_email(email):
        return users.find_one({'email': email})

    @staticmethod
    def verify_password(user, password):
        return check_password_hash(user['password'], password)

    @staticmethod
    def serialize_user(user):
        if not user:
            return None

        # Create a copy to avoid modifying the original
        user_data = user.copy()

        # Convert special types
        user_data['_id'] = str(user_data['_id'])

        if 'birthdate' in user_data and isinstance(user_data['birthdate'], datetime):
            user_data['birthdate'] = user_data['birthdate'].isoformat()

        if 'created_at' in user_data and isinstance(user_data['created_at'], datetime):
            user_data['created_at'] = user_data['created_at'].isoformat()

        return user_data