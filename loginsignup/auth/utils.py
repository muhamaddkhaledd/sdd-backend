from flask_jwt_extended import create_access_token
from loginsignup.auth.models import User


def authenticate_user(email, password):
    user = User.find_by_email(email)
    if user and User.verify_password(user, password):
        # Serialize user data
        user_data = User.serialize_user(user)

        # Remove sensitive data
        user_data.pop('password', None)

        access_token = create_access_token(identity=str(user['_id']))
        return {
            'access_token': access_token,
            'user': user_data
        }, 200
    return {'message': 'Invalid credentials'}, 401