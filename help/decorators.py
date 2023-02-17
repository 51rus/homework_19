from flask import request
from flask_restx import abort
import jwt

from help.constants import ALGO, SECRET


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split('Bearer')[-1]

        try:
            jwt.decode(token, SECRET, algorithms=[ALGO])
        except Exception as e:
            print('JWT Decode Exception', e)
            abort(401)

        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split('Bearer')[-1]

        try:
            user = jwt.decode(token, SECRET, algorithms=[ALGO])
            if user['role'] != 'admin':
                return 'You are not admin'
        except Exception as e:
            print('JWT Decode Exception', e)
            abort(401)

        return func(*args, **kwargs)

    return wrapper
