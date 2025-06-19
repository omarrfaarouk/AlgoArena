from flask import Blueprint, request, jsonify
from datetime import datetime
from bson import ObjectId
from . import mongo

bp = Blueprint('submissions', __name__, url_prefix='/submissions')

@bp.route('/', methods=['POST'])
def submit_code():
    """Handle code submissions with robust validation"""
    # Validate request
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
        
    data = request.get_json()
    
    # Required fields check
    required = ['code', 'language']
    if missing := [field for field in required if field not in data]:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    # Validate language
    valid_languages = ['python', 'javascript', 'java']
    if data['language'].lower() not in valid_languages:
        return jsonify({"error": f"Invalid language. Choose from: {valid_languages}"}), 400

    # Create submission
    submission = {
        "user_id": "temp_user",
        "code": data['code'],
        "language": data['language'].lower(),
        "status": "queued",  # New state flow: queued -> processing -> completed/failed
        "execution_time": None,  # Will store results later
        "memory_usage": None,
        "timestamp": datetime.utcnow(),
        "results": []
    }

    try:
        result = mongo.db.submissions.insert_one(submission)
        return jsonify({
            "status": "success",
            "submission_id": str(result.inserted_id),
            "queue_position": mongo.db.submissions.count_documents({"status": "pending"})
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/<submission_id>/status', methods=['GET'])
def get_status(submission_id):
    """Check submission status and position"""
    try:
        sub = mongo.db.submissions.find_one(
            {"_id": ObjectId(submission_id)},
            {"status": 1, "timestamp": 1}
        )
        if not sub:
            return jsonify({"error": "Not found"}), 404
            
        return jsonify({
            "status": sub["status"],
            "position": mongo.db.submissions.count_documents({
                "status": "queued",
                "timestamp": {"$lt": sub["timestamp"]}
            }),
            "wait_time_seconds": (datetime.utcnow() - sub["timestamp"]).total_seconds()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route('/')
def home():
    return "AlgoArena is running! 🚀"