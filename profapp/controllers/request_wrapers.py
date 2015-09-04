from functools import wraps
from flask import jsonify, request, g, abort
#from ..models.company import Right
from functools import reduce


def json(func):
    @wraps(func)
    def function_with_parent(*args, **kwargs):
        # try:
            ret = func(request.json)
            return jsonify({'result': ret, 'ok': True, 'error_code': 'ERROR_NO_ERROR'})
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


# make check for user groups!!!
def can_global(*rights_lambda_rule, **kwargs):
    rez = reduce(
        lambda x, y:
        x or y[list(y.keys())[0]](**kwargs), rights_lambda_rule, False)
    return rez


def check_rights(*rights_lambda_rule):
    # (rights, lambda_func) = rights_lambda_rule.items()[0]
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not can_global(*rights_lambda_rule, **kwargs):
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator
