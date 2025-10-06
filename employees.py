from flask import Blueprint, request, current_app
from models.employees import format_employee
from bson.objectid import ObjectId

emp_bp = Blueprint('employees', __name__)

@emp_bp.route('/', methods=['GET'])
def list_employees():
    db = current_app.db
    docs = list(db.employees.find({}))
    return {'employees': [format_employee(d) for d in docs]}

@emp_bp.route('/', methods=['POST'])
def create_employee():
    data = request.json or {}
    name = data.get('name'); email = data.get('email'); dept_id = data.get('dept_id')
    if not name or not email or not dept_id:
        return {'msg':'name, email, dept_id required'}, 400
    db = current_app.db
    try:
        oid = ObjectId(dept_id)
    except Exception:
        return {'msg':'invalid dept_id'}, 400
    doc = {'name':name,'email':email,'dept_id':oid,'role': data.get('role','employee')}
    db.employees.insert_one(doc)
    return {'msg':'created'}, 201

@emp_bp.route('/<id>', methods=['PUT'])
def update_employee(id):
    data = request.json or {}
    db = current_app.db
    db.employees.update_one({'_id': ObjectId(id)}, {'$set': data})
    return {'msg':'updated'}
