from flask import abort

def has_right(*args):
    if args[0]:
        pass
    else:
        return abort(403)