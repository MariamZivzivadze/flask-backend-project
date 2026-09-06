"""Flask application entry point: routes, config, and error handlers."""

import os
from dotenv import load_dotenv
from flask import Flask, request, render_template
from errors import InvalidCredentialsError, UserAlreadyExistsError
from models import User
from auth import auth_bp
from extensions import db, bcrypt, limiter
from errors import MissingFieldError

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
limiter.init_app(app)
db.init_app(app)
bcrypt.init_app(app)
app.register_blueprint(auth_bp)

with app.app_context():
    db.create_all()

@app.errorhandler(InvalidCredentialsError)   
def handle_invalid_credentials(error):
    return {"error": str(error)}, 401

@app.errorhandler(UserAlreadyExistsError)
def handle_user_already_exists(error):
    return {"error": str(error)}, 409

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/api/users")
def get_users():
    users = User.query.all()
    return [{"id": u.id, "name": u.name, "email": u.email} for u in users]

@app.errorhandler(MissingFieldError)
def handle_missing_field(error):
    return {"error": str(error)}, 400

@app.route("/api/posts", methods=["POST"])
def create_post():
    data = request.get_json(silent=True)
    if not data or not all(k in data for k in ("title", "content", "user_id")):
        raise MissingFieldError("Request must include title, content, and user_id")

    new_post = Post(title=data['title'], content=data['content'], user_id=data['user_id'])
    db.session.add(new_post)
    db.session.commit()
    return {"message": f"Post '{new_post.title}' created", "id": new_post.id}, 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
  

