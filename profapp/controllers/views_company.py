from .blueprints import company_bp
from flask import render_template, request, url_for, g, redirect
from db_init import db_session
from ..models.company import Company
from ..models.users import User
from .views_filemanager import file_query
from ..models.user_company_role import UserCompanyRole

@company_bp.route('/<string:id>/', methods=['GET', 'POST'])
def company(id):

    company = Company()
    companies = company.query_all_companies(id=id)

    return render_template('company.html',
                           companies=companies
                           )

@company_bp.route('/add_company/', methods=['GET', 'POST'])
def add_company():

    if request.method != 'GET':
        company = Company()
        company.add_comp(data=request.form)
        companies = company.query_all_companies(id=g.user.id)

        return redirect(url_for('company.company', id=g.user.id))

    return render_template('add_company.html')
