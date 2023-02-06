from flask import current_app, abort, request
from app.models.user import User
from functools import wraps
import traceback
import jwt


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return {
                'error': True,
                'success': False,
                'message': 'Unauthorized'
            }, 401

        try:
            data = jwt.decode(token, current_app.config.get("SECRET_KEY"), algorithms=['HS256'])
            current_user = User().get_by_id(data['user']['_id'])

            if current_user is None:
                return {
                    'error': True,
                    'success': False,
                    'message': 'Unauthorized'
                }, 401

            if current_user['status'] == 0:
                abort(403)

        except Exception:
            traceback.print_exc()
            return {
                'error': True,
                'success': False,
                'message': 'Error in server'
            }, 500

        return f(current_user, *args, **kwargs)
    return decorated
