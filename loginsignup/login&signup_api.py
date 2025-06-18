from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from auth.routes import initialize_routes
import os
from dotenv import load_dotenv
from auth.models import JSONEncoder

load_dotenv()

app = Flask(__name__)
app.json_encoder = JSONEncoder
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
api = Api(app)
jwt = JWTManager(app)

# Initialize routes
initialize_routes(api)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)