from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from extensions import db
from models import User
from datetime import datetime

main = Blueprint("main", __name__)

# -------------------------
# HTML ROUTES (Forms)
# -------------------------

@main.route("/")
def index():
    users = User.query.all()
    return render_template("index.html", users=users)

@main.route("/add", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        new_user = User(name=name, email=email, password=password, joined_on=datetime.utcnow())
        db.session.add(new_user)
        db.session.commit()
        flash("User added successfully!", "success")
        return redirect(url_for("main.index"))

    return render_template("add_user.html")

@main.route("/update/<int:id>", methods=["GET", "POST"])
def update_user(id):
    user = User.query.get_or_404(id)
    if request.method == "POST":
        user.name = request.form["name"]
        user.email = request.form["email"]
        user.password = request.form["password"]
        db.session.commit()
        flash("User updated successfully!", "info")
        return redirect(url_for("main.index"))

    return render_template("update_user.html", user=user)

@main.route("/delete/<int:id>")
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully!", "danger")
    return redirect(url_for("main.index"))

# -------------------------
# API ROUTES (JSON)
# -------------------------

# GET all users
@main.route("/api/users", methods=["GET"])
def get_users_api():
    users = User.query.all()
    return jsonify([
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "joined_on": u.joined_on
        } for u in users
    ])

# POST - create new user
@main.route("/api/users", methods=["POST"])
def create_user_api():
    data = request.get_json()

    if not data or not data.get("name") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing required fields"}), 400

    new_user = User(
        name=data["name"],
        email=data["email"],
        password=data["password"],
        joined_on=datetime.utcnow()
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User added successfully!"}), 201

# PUT - update user
@main.route("/api/users/<int:id>", methods=["PUT"])
def update_user_api(id):
    user = User.query.get_or_404(id)
    data = request.get_json()

    if "name" in data:
        user.name = data["name"]
    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        user.password = data["password"]

    db.session.commit()
    return jsonify({"message": "User updated successfully!"})

# DELETE - delete user
@main.route("/api/users/<int:id>", methods=["DELETE"])
def delete_user_api(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"})
