from flask import request, current_app as app
from flask_restful import abort
import jwt
from functools import wraps
from applications.models import User

def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {'error': 'Token is not passed'}, 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            user_id = data['user_id']
            user = User.query.get(user_id)
            if user and user.is_admin != '1':
                return {'error': 'Admin access required'}, 403
        except (jwt.ExpiredSignatureError, jwt.DecodeError):          
            return {'error': 'Token is invalid'}, 401
        
        return f(*args, **kwargs)
    return decorated


def user_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            abort(401, message='Token is not passed')

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            user_id = data['user_id']
            user = User.query.get(user_id)
            if user and user.is_admin != '0':
                abort(403, message='User access required')
        except (jwt.ExpiredSignatureError, jwt.DecodeError):
            return {'message': 'Token is invalid'}, 401
        
        return f(*args, **kwargs)
    
    return decorated
