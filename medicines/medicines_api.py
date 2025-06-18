from flask import Flask, jsonify ,Blueprint
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from bson import ObjectId

# Load environment variables
load_dotenv()

medicines_bp = Blueprint('medicines', __name__)

# MongoDB Configuration
mongo_uri = os.getenv("MONGO_URI")
db_name = 'medical_db'
collection_name = 'medicines'

# MongoDB Connection
client = MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]

# Helper to convert ObjectId to string for JSON
def convert_objectid(doc):
    doc['_id'] = str(doc['_id'])
    return doc

@medicines_bp.route('/medicines', methods=['GET'])
def get_all_medicines():
    medicines = list(collection.find())  # fetch all fields
    medicines = [convert_objectid(med) for med in medicines]
    return jsonify(medicines)

if __name__ == '__main__':
    medicines_bp.run(host="0.0.0.0", port=5002,debug=True)
