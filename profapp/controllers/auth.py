from flask import jsonify
from .users_blueprint import users_bp

@users_bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    return jsonify({'a': 'b'})


@users_bp.route('/login/', methods=['GET', 'POST'])
def login():
    return jsonify({'c': 'd'})