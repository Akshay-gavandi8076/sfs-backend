from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models.user_model import users_collection

auth_bp = Blueprint("auth_bp", __name__)

# Register User (Student/Admin)
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "student")  # Default to student

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    # Check if user already exists
    if users_collection.find_one({"email": email}):
        return jsonify({"error": "Email already exists"}), 400

    hashed_password = generate_password_hash(password)

    user = {
        "username": username,
        "email": email,
        "password": hashed_password,
        "role": role,
        "courses": []
    }

    users_collection.insert_one(user)
    return jsonify({"message": "User registered successfully!"}), 201


# Login User
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    user = users_collection.find_one({"email": email})
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Identity must be string! Store user ID as string
    access_token = create_access_token(
        identity=str(user["_id"]),
        additional_claims={
            "role": user["role"],
            "email": user["email"]
        }
    )

    return jsonify({
        "token": access_token,
        "role": user["role"]
    }), 200
