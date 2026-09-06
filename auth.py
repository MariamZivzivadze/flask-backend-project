"""Flask application entry point: routes, config, and error handlers."""

from flask import Blueprint, request
from models import User
from errors import InvalidCredentialsError, MissingFieldError, UserAlreadyExistsError
from extensions import db, bcrypt, limiter

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True)
    if not data or not all(k in data for k in ("name", "email", "password")):
        raise MissingFieldError("Request must include name, email, and password")

    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        raise UserAlreadyExistsError("A user with this email already exists")

    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(name=data['name'], email=data['email'], password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return {"message": f"Welcome, {new_user.name}! Saved with ID {new_user.id}"}, 201

@auth_bp.route("/api/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    data = request.get_json(silent=True)
    if not data or not all(k in data for k in ("email", "password")):
        raise MissingFieldError("Request must include email and password")

    user = User.query.filter_by(email=data['email']).first()
    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        raise InvalidCredentialsError("Invalid email or password")
    return {"message": f"Welcome back, {user.name}!"}, 200