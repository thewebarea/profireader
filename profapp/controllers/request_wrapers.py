from functools import wraps
from flask import jsonify, request, g, abort
from ..models.company import Right

def json(func):
    @wraps(func)
    def function_with_parent(*args, **kwargs):
        # try:
            return jsonify({'ok': True, 'error_code': 'ERROR_NO_ERROR', 'result': func(*args, **kwargs)})
        # except Exception:
        #     return jsonify({'ok': False, 'error_code': -1, 'result': "unknown error"})
    return function_with_parent

def parent_folder(func):
    @wraps(func)
    def function_with_parent(*args, **kwargs):
        parent_id = (None if (request.json['params']['parent_id'] == '') else (request.json['params']['parent_id']))
        kwargs['parent_id'] = parent_id
        return func(*args, **kwargs)
    return function_with_parent

def replace_brackets(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if kwargs:
            for ch in ['{', '}', ' ']:
                for key in kwargs:
                    if ch in kwargs[key]:
                        kwargs[key] = kwargs[key].replace(ch, "")
        return func(*args, **kwargs)
    return wrapper

def check_rights(rights):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            if not set(rights) < set(Right.permissions(user_id=g.user_dict['id'], comp_id=kwargs['company_id'])):
                return abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator
