from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.student_model import students_collection
from models.admin_model import admins_collection
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId

auth_bp = Blueprint("auth", __name__)

# Register Student
@auth_bp.route("/register", methods=["POST"])
def register_student():
    data = request.get_json()
    if not all(k in data for k in ("email", "password", "name")):
        return jsonify({"msg": "Missing fields"}), 400

    if students_collection.find_one({"email": data["email"]}):
        return jsonify({"msg": "Student already exists"}), 409

    student = {
        "name": data["name"],
        "email": data["email"],
        "password": generate_password_hash(data["password"])
    }
    students_collection.insert_one(student)
    return jsonify({"msg": "Student registered successfully"}), 201

# Register Admin
@auth_bp.route("/register/admin", methods=["POST"])
def register_admin():
    data = request.get_json()
    if not all(k in data for k in ("email", "password", "name")):
        return jsonify({"msg": "Missing fields"}), 400

    if admins_collection.find_one({"email": data["email"]}):
        return jsonify({"msg": "Admin already exists"}), 409

    admin = {
        "name": data["name"],
        "email": data["email"],
        "password": generate_password_hash(data["password"])
    }
    admins_collection.insert_one(admin)
    return jsonify({"msg": "Admin registered successfully"}), 201

# Login Student
@auth_bp.route("/login", methods=["POST"])
def login_student():
    data = request.get_json()
    student = students_collection.find_one({"email": data["email"]})
    if not student or not check_password_hash(student["password"], data["password"]):
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(student["_id"]), additional_claims={"role": "student"})
    return jsonify({"access_token": access_token}), 200

# Login Admin
@auth_bp.route("/login/admin", methods=["POST"])
def login_admin():
    data = request.get_json()
    admin = admins_collection.find_one({"email": data["email"]})
    if not admin or not check_password_hash(admin["password"], data["password"]):
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(admin["_id"]), additional_claims={"role": "admin"})
    return jsonify({"access_token": access_token}), 200


# from flask import Blueprint, request, jsonify
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_jwt_extended import create_access_token
# from models.user_model import users_collection

# auth_bp = Blueprint("auth_bp", __name__)

# # Register User (Student/Admin)
# @auth_bp.route("/register", methods=["POST"])
# def register():
#     data = request.json
#     username = data.get("username")
#     email = data.get("email")
#     password = data.get("password")
#     role = data.get("role", "student")  # Default to student

#     if not username or not email or not password:
#         return jsonify({"error": "Missing required fields"}), 400

#     # Check if user already exists
#     if users_collection.find_one({"email": email}):
#         return jsonify({"error": "Email already exists"}), 400

#     hashed_password = generate_password_hash(password)

#     user = {
#         "username": username,
#         "email": email,
#         "password": hashed_password,
#         "role": role,
#         "courses": []
#     }

#     users_collection.insert_one(user)
#     return jsonify({"message": "User registered successfully!"}), 201


# # Login User
# @auth_bp.route("/login", methods=["POST"])
# def login():
#     data = request.json
#     email = data.get("email")
#     password = data.get("password")

#     if not email or not password:
#         return jsonify({"error": "Missing email or password"}), 400

#     user = users_collection.find_one({"email": email})
#     if not user:
#         return jsonify({"error": "Invalid credentials"}), 401

#     if not check_password_hash(user["password"], password):
#         return jsonify({"error": "Invalid credentials"}), 401

#     # Identity must be string! Store user ID as string
#     access_token = create_access_token(
#         identity=str(user["_id"]),
#         additional_claims={
#             "role": user["role"],
#             "email": user["email"]
#         }
#     )

#     return jsonify({
#         "token": access_token,
#         "role": user["role"]
#     }), 200
