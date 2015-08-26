from flask import abort

def has_right(*args):
    if args[0]:
        pass
    else:
        # raise Exception("authorization failed")
        pass
        # return abort(403)