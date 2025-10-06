from flask import Blueprint, request, current_app
from werkzeug.security import check_password_hash
import bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')
    role = data.get('role','user')
    if not username or not password:
        return {'msg':'username and password required'}, 400
    db = current_app.db
    if db.users.find_one({'username':username}):
        return {'msg':'username exists'}, 400
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    db.users.insert_one({'username':username,'password_hash':pw_hash,'role':role})
    return {'msg':'user created'}, 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return {'msg':'username and password required'}, 400
    db = current_app.db
    user = db.users.find_one({'username':username})
    if not user:
        return {'msg':'invalid credentials'}, 401
    if not bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
        return {'msg':'invalid credentials'}, 401
    access = create_access_token(identity=str(user['_id']), additional_claims={'role':user.get('role')}, expires_delta=timedelta(days=1))
    return {'access_token': access, 'user': {'username': user['username'], 'role': user.get('role')}}
