from functools import wraps
from flask import jsonify, request, g, abort
from ..models.company import Right
from sqlalchemy.orm import relationship, backref, make_transient, class_mapper
import datetime
from db_init import Base

def json(func):
    @wraps(func)
    def function_with_parent(*args, **kwargs):
        # try:
            kwargs['json'] = request.json
            ret = func(*args, **kwargs)
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

def check_rights(rights):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            if not set(rights) < set(Right.permissions(user_id=g.user_dict['id'], comp_id=kwargs['company_id'])):
                return abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def convert_col_to_arrays(*args):
    a = list(args)
    if isinstance(a[0], dict):
        ret = a[0] if len(a) == 1 else False
        if not isinstance(ret, dict):
            raise ValueError("object_to_dict expect as arguments columns in form 'column' or '*' or 'relation.*.column'")
        return ret

    else:
        columns = {}
        relationships = {}
        for argument in a:
            columnsdevided = argument.split('.')
            if len(columnsdevided) == 1:
                columns[argument] ={}
                curcol = columns
                for simplecolumn in columnsdevided:
                    if simplecolumn not in curcol:
                        curcol[simplecolumn] = {}
                    curcol = curcol[simplecolumn]
            else:
                pass
        return columns

def need_we_column(name, arr, is_relationship = False):
    realname = name if name in arr else '*'
    if not is_relationship:
        if realname in arr:
            if len(arr[realname])>0:
                raise ValueError("you ask for sub-attribute of Column instance `%s` (not Relationship)" % (realname, ))
            return True
        else:
            return False
    else:
        if realname in arr:
            if len(arr[name]) == 0:
                raise ValueError("You ask for Relationship `%s` instance, but don't ask for any sun-attribute in it" % (realname, ))
            return arr[name]
        else:
            return False


def object_to_dict(obj, *args):
        whatweneed = convert_col_to_arrays(*args)
        ret={}
        columns = class_mapper(obj.__class__).columns
        realations = class_mapper(obj.__class__).relationships.items()
        get_key_value = lambda o: o.isoformat() if isinstance(o, datetime.datetime) else o
        for col in columns:
            if need_we_column(col.key, whatweneed):
                ret[col.key] = get_key_value(getattr(obj, col.key))
            if col.key in whatweneed:
                del whatweneed[col.key]

        for relationname, relation in realations:
            whatweneedinnextlevel = need_we_column(relationname, whatweneed)
            # if need_we_column(relationname, whatweneed):
            # whatweneedinnextlevel = need_we_column(relationname, whatweneed)
                # whatweneed[relationname] if relationname in whatweneed else whatweneed['*']
            related_obj = getattr(obj, relationname)
            if relation.uselist:
                ret[relationname] = [object_to_dict(child, whatweneedinnextlevel) for child in related_obj]
            else:
                ret[relationname] = object_to_dict(related_obj, whatweneedinnextlevel)
            if relationname in whatweneed:
                del whatweneed[relationname]

        return ret
        ret = dict([get_key_value(col.key) for col in columns if col.key in whatweneed or '*' in whatweneed])

        # for column in
        # for name, relation in class_mapper(obj.__class__).relationships.items():
        #     if name in show or show == '*':
        #         related_obj = getattr(obj, name)
        #         if show == '*':
        #             innextlevel = ['id']
        #         else:
        #             innextlevel = ['id'] if show[name] == True else show[name]
        #         if relation.uselist:
        #             ret[name] = [object_to_dict(child, innextlevel) for child in related_obj]
        #         else:
        #             ret[name] = object_to_dict(related_obj, innextlevel)
        #
        #
        # columns = class_mapper(obj.__class__).columns
        # get_key_value = lambda c: (c, getattr(obj, c).isoformat()) if isinstance(getattr(obj, c), datetime.datetime) else (c, getattr(obj, c))
        # ret = dict([get_key_value(col.key) for col in columns if col.key in show or show == '*'])
        #
        # for name, relation in class_mapper(obj.__class__).relationships.items():
        #     if name in show or show == '*':
        #         related_obj = getattr(obj, name)
        #         if show == '*':
        #             innextlevel = ['id']
        #         else:
        #             innextlevel = ['id'] if show[name] == True else show[name]
        #         if relation.uselist:
        #             ret[name] = [object_to_dict(child, innextlevel) for child in related_obj]
        #         else:
        #             ret[name] = object_to_dict(related_obj, innextlevel)




        #
        #
        # ret = {}
        # if isinstance(fields, dict):
        #     for fieldname in fields:
        #         atr = getattr(obj, fieldname)
        #         if isinstance(atr, list):
        #             ret[fieldname] = [object_to_dict(i, fields[fieldname]) for i in atr]
        #         elif isinstance(atr, Base):
        #             ret[fieldname] = object_to_dict(atr, fields[fieldname])
        #         else:
        #             ret[fieldname] = atr
        #
        return ret


# mapper = class_mapper(obj.__class__)
        # columns = [column.key for column in mapper.columns]
        # get_key_value = lambda c: (c, getattr(obj, c).isoformat()) if isinstance(getattr(obj, c), datetime.datetime) else (c, getattr(obj, c))
        # out = dict(map(get_key_value, columns))
        # for name, relation in mapper.relationships.items():
        #     related_obj = getattr(obj, name)
        #     if relation not in found or relation.uselist:
        #         found.add(relation)
        #         print((obj, name, relation, relation.uselist))
        #         if related_obj is not None:
        #             if relation.uselist:
        #                 out[name] = [object_to_dict(child, found) for child in related_obj]
        #             else:
        #                 out[name] = object_to_dict(related_obj, found)
        #     # else:
        #     #     if relation.uselist:
        #     #         out[name] = [object_to_dict(child, found) for child in related_obj]
        #     #     else:
        #     #         out[name] = object_to_dict(related_obj, found)
        #
        # return out