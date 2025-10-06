from flask import Blueprint, request, current_app
from bson.objectid import ObjectId
from datetime import datetime

leaves_bp = Blueprint('leaves', __name__)

# Request a leave
@leaves_bp.route('/', methods=['POST'])
def request_leave():
    data = request.json or {}
    emp_id = data.get('emp_id')
    start = data.get('start_date')
    end = data.get('end_date')

    if not emp_id or not start or not end:
        return {'msg': 'emp_id,start_date,end_date required'}, 400

    try:
        oid = ObjectId(emp_id)
    except Exception:
        return {'msg': 'invalid emp_id'}, 400

    db = current_app.db
    db.leave_requests.insert_one({
        'emp_id': oid,
        'start_date': datetime.fromisoformat(start),
        'end_date': datetime.fromisoformat(end),
        'status': 'pending'
    })
    return {'msg': 'leave requested'}, 201


# Get leaves of one employee
@leaves_bp.route('/<emp_id>', methods=['GET'])
def list_leaves(emp_id):
    db = current_app.db
    docs = list(db.leave_requests.find({'emp_id': ObjectId(emp_id)}))
    out = []
    for d in docs:
        out.append({
            'id': str(d['_id']),
            'start_date': d['start_date'].isoformat(),
            'end_date': d['end_date'].isoformat(),
            'status': d['status']
        })
    return {'leaves': out}


# ✅ Get all leave requests
@leaves_bp.route('/', methods=['GET'])
def list_all_leaves():
    db = current_app.db
    docs = list(db.leave_requests.find().sort('start_date', -1).limit(100))
    out = []
    for d in docs:
        out.append({
            'id': str(d['_id']),
            'emp_id': str(d['emp_id']),
            'start_date': d['start_date'].isoformat(),
            'end_date': d['end_date'].isoformat(),
            'status': d['status']
        })
    return {'leaves': out}
