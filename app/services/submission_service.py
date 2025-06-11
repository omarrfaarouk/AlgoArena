from datetime import datetime
from .. import mongo  # or `from flask import current_app` + use `current_app.db`

def create_submission(user_id, code, language):
    """Save submission to MongoDB and return its ID."""
    result = mongo.db.submissions.insert_one({
        "user_id": user_id,
        "code": code,
        "language": language,
        "status": "pending",
        "created_at": datetime.utcnow()
    })
    return str(result.inserted_id)  # Convert ObjectId to string

def get_submissions(limit=10):
    """Fetch recent submissions."""
    submissions = list(mongo.db.submissions.find().sort("created_at", -1).limit(limit))
    for sub in submissions:  # Convert ObjectId to string
        sub["_id"] = str(sub["_id"])
    return submissions