from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {"id": self.id, "username": self.username, "email": self.email}


with app.app_context():
    db.create_all()


# Test Route
@app.route("/test", methods=["GET"])
def test():
    return make_response(jsonify({"message": "test route"}), 200)


# Create User
@app.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        new_user = User(username=data["username"], email=data["email"])
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({"message": "user created"}), 201)
    except:
        return make_response(jsonify({"message": "error creating user"}), 500)


# Get All Users
@app.route("/users", methods=["GET"])
def get_users():
    try:
        users = User.query.all()
        return make_response(jsonify([user.json() for user in users]), 200)
    except:
        return make_response(jsonify({"message": "error getting users"}), 500)


# Get User By ID
@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return make_response(jsonify({"user": user.json()}), 200)
        return make_response(jsonify({"message": "user not found"}), 404)
    except:
        return make_response(jsonify({"message": "error getting user"}), 500)


# Update User
@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            data = request.get_json()
            user.username = data["username"]
            user.email = data["email"]
            db.session.commit()
            return make_response(jsonify({"message": "user updated"}), 200)
        return make_response(jsonify({"message": "user not found"}), 404)
    except:
        return make_response(jsonify({"message": "error updating user"}), 500)


# Delete User
@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({"message": "user deleted"}), 200)
        return make_response(jsonify({"message": "user not found"}), 404)
    except:
        return make_response(jsonify({"message": "error deleting user"}), 500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="4000", debug=True)
