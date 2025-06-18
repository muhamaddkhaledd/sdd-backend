from flask import Flask, jsonify ,Blueprint
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from bson import ObjectId

load_dotenv()

diseases_bp = Blueprint('diseases', __name__)

# MongoDB Configuration
mongo_uri = os.getenv("MONGO_URI")
db_name = 'medical_db'
collection_name = 'skin_diseases'

# MongoDB Connection
client = MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]

# Helper to convert ObjectId to string for JSON
def convert_objectid(doc):
    doc['_id'] = str(doc['_id'])
    return doc

@diseases_bp.route('/diseases', methods=['GET'])
def get_all_diseases():
    diseases = list(collection.find())  # fetch all fields
    diseases = [convert_objectid(dis) for dis in diseases]
    return jsonify(diseases)

if __name__ == '__main__':
    diseases_bp.run(host="0.0.0.0", port=5003,debug=True)
