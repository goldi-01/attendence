from flask import Blueprint, request, current_app
from bson.objectid import ObjectId
from datetime import datetime

att_bp = Blueprint('attendance', __name__)

# Mark attendance
@att_bp.route('/mark', methods=['POST'])
def mark():
    data = request.json or {}
    emp_id = data.get('emp_id')
    status = data.get('status', 'present')
    date = data.get('date')

    if not emp_id:
        return {'msg': 'emp_id required'}, 400
    try:
        oid = ObjectId(emp_id)
    except Exception:
        return {'msg': 'invalid emp_id'}, 400

    d = datetime.utcnow() if not date else datetime.fromisoformat(date)
    db = current_app.db
    db.attendance_logs.insert_one({'emp_id': oid, 'date': d, 'status': status})
    return {'msg': 'marked'}, 201


# Get attendance for one employee
@att_bp.route('/<emp_id>', methods=['GET'])
def list_attendance(emp_id):
    db = current_app.db
    docs = list(
        db.attendance_logs.find({'emp_id': ObjectId(emp_id)}).sort('date', -1).limit(50)
    )
    out = []
    for d in docs:
        out.append({
            'id': str(d['_id']),
            'date': d['date'].isoformat(),
            'status': d['status']
        })
    return {'attendance': out}


# ✅ Get attendance for all employees
@att_bp.route('/', methods=['GET'])
def list_all_attendance():
    db = current_app.db
    docs = list(db.attendance_logs.find().sort('date', -1).limit(100))
    out = []
    for d in docs:
        out.append({
            'id': str(d['_id']),
            'emp_id': str(d['emp_id']),
            'date': d['date'].isoformat(),
            'status': d['status']
        })
    return {'attendance': out}
