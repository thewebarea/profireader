from .blueprints import company_bp
from flask import render_template, request, url_for, g, redirect
from db_init import db_session
from ..models.company import Company
from ..models.users import User
from .views_filemanager import file_query
from ..models.user_company_role import UserCompanyRole

@company_bp.route('/<string:user_id>')
def show_companies(user_id):
    companies = db_session.query(Company).filter_by(user_id=user_id).all()
    query_companies = db_session.query(UserCompanyRole).\
        filter_by(user_id=user_id).all()
    for company in query_companies:
        companies = companies + \
            db_session.query(Company).\
            filter_by(id=company.company_id).all()

    return render_template('company.html',
                           companies=companies
                           )

@company_bp.route('/add_company/', methods=['GET', 'POST'])
def add_company():
    if request.method != 'GET':
        company = Company()
        company.user_id = g.user_init.get_id()
        company.name = request.form['name']
        db_session.add(company)
        db_session.commit()
        return redirect(url_for('company.show_company', id=g.user_dict.id))
    return render_template('add_company.html')
