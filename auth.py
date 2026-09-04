from flask import Blueprint, request
from flask_bcrypt import Bcrypt

auth_bp = Blueprint('auth', __name__)