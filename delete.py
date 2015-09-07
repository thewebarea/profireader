def y(*args):
    print(args)
    print(*args)
    print(*[args])
    return


def x(*args):
    print('args = ', args)
    y(args)
    print('******************************************')
    print('*args = ', *args)
    y(*args)
    print('++++++++++++++++++++++++++++++++++++++++++')
    print('*[args] = ', *[args])
    y(*[args])
    return args

args = {'a': 'b'}
x(*args)

#print('======================================================')

#x('a', 'b')


def f1():
    def f2(x1, x2):
        return x1 + x2
    return f2

x = f1()

y = x(2, 3)
print(y)
print('*****************')

from functools import reduce

z = reduce(lambda x, y: x + y, [1])
print(z)
print('*****************')
print('*****************')

arg = 0

from random import choice


def g(x):
    r = choice([True, False])
    return r


rights_lambda_rule = ({frozenset(): g}, {frozenset(): g}, )


def f(x, y):
    print(list(x.keys())[0])
    print(x[list(x.keys())[0]])
    print(x[list(x.keys())[0]](arg))
    return x[list(x.keys())[0]](arg) or y[list(y.keys())[0]](arg)

rez = reduce(f, rights_lambda_rule
    #, {frozenset(): lambda **kwargs2: False}
)

print(rez)
print(rez)

print('*****************************888')


def rights_and(rights_in_integer_1, rights_in_integer_2):
    st1 = \
        list(map(int,
                 list(bin(rights_in_integer_1)[2:].rjust(63, '0')[::-1])))
    st2 = \
        list(map(int,
                 list(bin(rights_in_integer_2)[2:].rjust(63, '0')[::-1])))

    st_zip = zip(st1, st2)
    return map(lambda x, y: x*y, st_zip)

rights_in_integer_1 = 12
rights_in_integer_2 = 653223
z = rights_and(rights_in_integer_1, rights_in_integer_2)

print(z)
