from .blueprints import front_bp
from flask import render_template, request, url_for, redirect
from ..models.company import Company
from ..models.portal import CompanyPortal


@front_bp.route('/', methods=['GET'])
def index():
    return '!!!'

