import json
from datetime import timedelta

import bson
from bson import ObjectId, json_util
from flask import Flask, jsonify, make_response, request
from flask_jwt_extended import (JWTManager, create_access_token,
                                create_refresh_token, get_jwt_identity,
                                jwt_required)
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "chesc bobr"
app.config["JWT_TOKEN_LOCATION"] = ["headers", "query_string"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
client = MongoClient(
    "mongodb+srv://igorby8881:7GgEv1vvmV99HuIs@cluster0.hbojcb0."
    "mongodb.net/?retryWrites=true&w=majority")
db = client["test_appdb"]
collection = db["users"]


@app.route('/registration', methods=["POST"])
def create_user():
    try:
        username = request.json["username"]
        email = request.json["email"]
        password = generate_password_hash(request.json["password"])

        if not username or not email or not password:
            return jsonify(message="Username, email, and password are required."), 400

        check = collection.find_one({"email": email})
        if check:
            return jsonify(message="User exists")
        else:
            user_info = dict(email=email,
                             password=password,
                             username=username,
                             )
            collection.insert_one(user_info)
            refresh_token = create_refresh_token(identity=email)
            access_token = create_access_token(identity=email)
        return jsonify(message="User created",
                       user=email,
                       refresh_token=refresh_token,
                       access_token=access_token,
                       username=username
                       ), 201
    except Exception as e:
        return jsonify(error="An error occurred", message=str(e)), 500


@app.route("/login", methods=["POST"])
def login():
    try:
        email = request.json["email"]
        password = request.json["password"]

        check = collection.find_one({"email": email})
        user = json.loads(json_util.dumps(collection.find_one({"email": email})))
        if check and check_password_hash(check["password"], password):
            access_token = create_access_token(identity=email)
            refresh_token = create_refresh_token(identity=email)
            return jsonify(
                message="User exists",
                access_token=access_token,
                refresh_token=refresh_token,
                user=user
            ), 200
        elif check and not check_password_hash(check["password"], password):
            return jsonify(message="Incorrect password"), 401
        else:
            return jsonify(message="Incorrect email"), 404
    except Exception as e:
        return jsonify(error="An error occurred", message=str(e)), 500


@app.route("/is_login", methods=["get"])
@jwt_required()
def is_login():
    return {"answer": True}


@app.route('/users', methods=['GET'])
@jwt_required()
def get_user():
    try:
        email = get_jwt_identity()
        user = collection.find_one({"email": email})
        if user:
            return make_response(json_util.dumps({"result": user})), 201
        else:
            return jsonify(message="User not found"), 401
    except bson.errors.InvalidId as e:
        return make_response(jsonify({"exception": str(e)})), 500


@app.route('/update_user/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        username = request.json["username"]
        password = request.json["password"]

        user = collection.find_one({'_id': ObjectId(user_id)})
        if user:
            collection.update_one({"_id": ObjectId(user_id)}, {"$set": {
                "username": username,
                "password": password,
            }})
            return jsonify(message="User updated"), 201
        else:
            return jsonify(message="User not found"), 401
    except bson.errors.InvalidId as e:
        return make_response(jsonify({"exception": str(e)})), 500


@app.route('/delete_user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        result = collection.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count == 0:
            return jsonify(message="User not found"), 401
        else:
            return jsonify(message="User deleted"), 201
    except bson.errors.InvalidId as e:
        return make_response(jsonify({"exception": str(e)})), 500


if __name__ == '__main__':
    app.run(debug=True)
