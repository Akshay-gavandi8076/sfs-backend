from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from models.feedback_model import feedback_collection
from models.course_model import courses_collection
from models.student_model import students_collection

feedback_bp = Blueprint("feedback", __name__)

@feedback_bp.route("/feedback", methods=["POST"])
@jwt_required()
def give_feedback():
    data = request.get_json()

    required_fields = ["course_id", "rating", "comment"]
    if not all(field in data for field in required_fields):
        return jsonify({"msg": "Missing fields"}), 400

    current_user = get_jwt_identity()
    student = students_collection.find_one({"_id": ObjectId(current_user)})

    if not student:
        return jsonify({"msg": "Only students can submit feedback"}), 403

    feedback = {
        "course_id": ObjectId(data["course_id"]),
        "student_id": ObjectId(current_user),
        "rating": int(data["rating"]),
        "comment": data["comment"]
    }

    feedback_collection.insert_one(feedback)
    return jsonify({"msg": "Feedback submitted successfully"}), 201

@feedback_bp.route("/feedbacks/<course_id>", methods=["GET"])
@jwt_required()
def get_feedbacks_for_course(course_id):
    feedbacks = list(feedback_collection.find({"course_id": ObjectId(course_id)}))
    
    for fb in feedbacks:
        fb["_id"] = str(fb["_id"])
        fb["student_id"] = str(fb["student_id"])
        fb["course_id"] = str(fb["course_id"])
    
    return jsonify(feedbacks), 200

# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from bson import ObjectId
# from models.feedback_model import feedback_collection
# from models.course_model import courses_collection
# from models.user_model import users_collection

# feedback_bp = Blueprint("feedback", __name__)

# @feedback_bp.route("/feedback", methods=["POST"])
# def give_feedback():
#     data = request.get_json()

#     required_fields = ["course_id", "student_id", "rating", "comment"]
#     if not all(field in data for field in required_fields):
#         return jsonify({"msg": "Missing fields"}), 400

#     feedback = {
#         "course_id": ObjectId(data["course_id"]),
#         "student_id": ObjectId(data["student_id"]),
#         "rating": int(data["rating"]),
#         "comment": data["comment"]
#     }

#     feedback_collection.insert_one(feedback)
#     return jsonify({"msg": "Feedback submitted successfully"}), 201

# @feedback_bp.route("/feedbacks/<course_id>", methods=["GET"])
# @jwt_required()
# def get_feedbacks_for_course(course_id):
#     feedbacks = list(feedback_collection.find({"course_id": ObjectId(course_id)}))
    
#     for fb in feedbacks:
#         fb["_id"] = str(fb["_id"])
#         fb["student_id"] = str(fb["student_id"])
#         fb["course_id"] = str(fb["course_id"])
    
#     return jsonify(feedbacks), 200
