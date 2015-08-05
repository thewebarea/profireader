from functools import wraps
from flask import jsonify, request

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