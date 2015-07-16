# It works as for Py2 as for Py3!!!
#
# http://python-future.org/quickstart.html
# see 'Installation' section
#
# The easiest way to write code valid for both Py2 and Py3 is
# to start each new module with these lines:
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *
from future import standard_library
standard_library.install_aliases()
# see also:
# http://python-future.org/what_else.html#what-else

from flask import url_for
from flask.ext.script import Manager
# for making scripts with Flask see documentation:
# http://flask-script.readthedocs.org/en/latest/

from profapp import create_app

app = create_app()
manager = Manager(app)

@manager.command
def list_routes():
    """ the solution was found here:
    http://stackoverflow.com/a/19116758/4388451
    and here
    http://stackoverflow.com/a/22651263/4388451

    Python 2.6+ / Python 3.3+ compatibility package: python-future
    http://python-future.org/overview.html

    to use it run: python manage.py list_routes"""
    import urllib.parse
    output = []
    st = '{:30s} {:25s} {}'
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        try:
            options = {}
            for arg in rule.arguments:
                options[arg] = "[{0}]".format(arg)

            url = url_for(rule.endpoint, **options)
            line = urllib.parse.unquote(st.format(rule.endpoint, methods, url))
        except:
            line = urllib.parse.unquote(st.format(rule.endpoint,
                                                  methods, rule))
        output.append(line)

    for line in sorted(output):
        print(line)

list_routes()
