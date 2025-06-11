from flask import Blueprint, request, jsonify
from app.services.submission_service import create_submission, get_submissions  # Changed from . to app

bp = Blueprint('main', __name__)

@bp.route('/submit', methods=['POST'])
def submit_code():
    data = request.get_json()  # Expects JSON: {"user_id": "123", "code": "print(42)", "language": "python"}
    submission_id = create_submission(
        user_id=data['user_id'],
        code=data['code'],
        language=data['language']
    )
    return jsonify({"submission_id": submission_id})

@bp.route('/submissions', methods=['GET'])
def list_submissions():
    submissions = get_submissions()
    return jsonify(submissions)

@bp.route('/')
def home():
    return "AlgoArena is running! 🚀"