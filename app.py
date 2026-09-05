import os
from dotenv import load_dotenv
from flask import Flask, request, render_template
from errors import InvalidCredentialsError, UserAlreadyExistsError
from extensions import db, bcrypt
from models import User
from auth import auth_bp

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

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

if __name__ == '__main__':
    app.run(debug=True)

