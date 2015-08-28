from functools import wraps
from flask import jsonify, request, g, abort
from ..models.company import Right

def json(func):
    @wraps(func)
    def function_json(*args, **kwargs):
        # try:
            ret = func(request.json)
            return jsonify({'result': ret, 'ok': True, 'error_code': 'ERROR_NO_ERROR'})
        # except Exception:
        #     return jsonify({'ok': False, 'error_code': -1, 'result': "unknown error"})
    return function_json

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

# def check_rights(rights):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#
#             if not set(rights) < set(Right.permissions(user_id=g.user_dict['id'], comp_id=kwargs['company_id'])):
#                 return abort(403)
#             return func(*args, **kwargs)
#         return wrapper
#     return decorator

def check_rights(**rulelam):
    # (rule_name, lambda_func) = rulelam.items()[0]
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            has = rulelam
            for x in has:
                has[x](**kwargs)
            return func(*args, **kwargs)
        return wrapper
    return decorator
