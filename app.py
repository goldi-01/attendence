from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# configuration from env
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret')

jwt = JWTManager(app)

# MongoDB client
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/devdb')
client = MongoClient(MONGO_URI)
db = client.get_default_database()

# register blueprints
from routes.auth import auth_bp
from routes.employees import emp_bp
from routes.attendance import att_bp
from routes.leaves import leaves_bp
from routes.admin import admin_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(emp_bp, url_prefix='/api/employees')
app.register_blueprint(att_bp, url_prefix='/api/attendance')
app.register_blueprint(leaves_bp, url_prefix='/api/leaves')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

# attach db to app for easy access in routes
app.db = db

@app.route('/')
def index():
    return {'status':'ok', 'msg':'MongoDB + Flask boilerplate running'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
