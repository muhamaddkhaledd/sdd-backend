from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# Load dotenv
load_dotenv()

# App setup
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
api = Api(app)
jwt = JWTManager(app)

# Import and register blueprints
from diseases.skin_diseases_api import diseases_bp
from history.history_api import diagnoses_bp
from medicines.medicines_api import medicines_bp
from loginsignup.auth.routes import initialize_routes

app.register_blueprint(diseases_bp)
app.register_blueprint(diagnoses_bp)
app.register_blueprint(medicines_bp)

# Initialize auth routes
initialize_routes(api)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
