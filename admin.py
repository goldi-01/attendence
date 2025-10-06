from flask import Blueprint, current_app
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/ping_db', methods=['GET'])
def ping_db():
    try:
        current_app.db.command('ping')
        return {'ok':True}
    except Exception as e:
        return {'ok':False, 'error': str(e)}, 500
