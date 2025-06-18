from flask import Flask, request, jsonify ,Blueprint
from pymongo import MongoClient
import base64
import os
from dotenv import load_dotenv
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId


# تحميل بيانات الاتصال من ملف .env
load_dotenv()


MONGO_URI = os.getenv('MONGO_URI')

# اتصال بقاعدة البيانات
client = MongoClient(MONGO_URI)
db = client["medical_db"]
collection = db["diagnoses"]

# إعداد التطبيق
diagnoses_bp = Blueprint('diagnoses', __name__)

#API لحفظ البيانات
@diagnoses_bp.route('/upload_diagnosis', methods=['POST'])
def upload_diagnosis():
    data = request.json

    required_fields = ['userid', 'disease_name', 'disease_explanation',
                       'confidence', 'disease_image', 'disease_heatmap']

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Create a new diagnosis object (without diagnosis_id yet)
    diagnosis_data = {
        "userid": data["userid"],
        "disease_name": data["disease_name"],
        "disease_explanation": data["disease_explanation"],
        "confidence": data["confidence"],
        "disease_image": data["disease_image"],
        "disease_heatmap": data["disease_heatmap"],
        "diagnose_time": datetime.utcnow().isoformat()
    }

    # Insert into MongoDB
    result = collection.insert_one(diagnosis_data)

    # Update the inserted document with its ID (saved as string)
    collection.update_one(
        {"_id": result.inserted_id},
        {"$set": {"diagnosis_id": str(result.inserted_id)}}
    )

    return jsonify({
        "message": "Diagnosis uploaded successfully.",
        "diagnosis_id": str(result.inserted_id)
    }), 201


#to delete diagnosis
@diagnoses_bp.route('/delete_diagnosis/<diagnosis_id>', methods=['DELETE'])
def delete_diagnosis(diagnosis_id):
    try:
        data = request.json  # User sends userid in the body
        userid = data.get("userid")
        if not userid:
            return jsonify({"error": "userid is required in request body."}), 400

        # Check if the diagnosis exists and belongs to this userid
        diagnosis = collection.find_one({
            "_id": ObjectId(diagnosis_id),
            "userid": userid
        })

        if not diagnosis:
            return jsonify({"error": "Diagnosis not found or access denied."}), 404

        # Proceed with deletion
        collection.delete_one({"_id": ObjectId(diagnosis_id)})
        return jsonify({"message": "Diagnosis deleted successfully."}), 200

    except InvalidId:
        return jsonify({"error": "Invalid diagnosis ID format."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500




#API لجلب بيانات مستخدم معين
@diagnoses_bp.route('/get_diagnoses/<userid>', methods=['GET'])
def get_diagnoses(userid):
    user_diagnoses = list(
        collection.find({"userid": userid}, {"_id": 0}).sort("diagnose_time", -1)
    )
    return jsonify({"datas": user_diagnoses}), 200


if __name__ == '__main__':
    diagnoses_bp.run(host="0.0.0.0", port=5001,debug=True)
