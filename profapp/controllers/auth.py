from flask import jsonify
from .blueprints import user_bp

@user_bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    return jsonify({'a': 'b'})


@user_bp.route('/login/', methods=['GET', 'POST'])
def login():
    return jsonify({'c': 'd'})