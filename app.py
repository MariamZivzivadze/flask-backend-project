import os
from dotenv import load_dotenv
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from errors import InvalidCredentialsError

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.errorhandler(InvalidCredentialsError)   
def handle_invalid_credentials(error):
    return {"error": str(error)}, 401

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json()
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(name=data['name'], email=data['email'], password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return {"message": f"Welcome, {new_user.name}! Saved with ID {new_user.id}"}

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user or not bcrypt.check_password_hash(user.password, data['password']):
        raise InvalidCredentialsError("Invalid email or password")
    return {"message": f"Welcome back, {user.name}!"}

@app.route("/api/users")
def get_users():
    users = User.query.all()
    return [{"id": u.id, "name": u.name, "email": u.email} for u in users]

if __name__ == '__main__':
    app.run(debug=True)

