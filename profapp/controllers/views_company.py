from .blueprints import company_bp
from flask import render_template, request, url_for, g, redirect
from ..models.company import Company


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

        return redirect(url_for('company.company', id=g.user.id))

    return render_template('add_company.html', id=g.user.id)

@company_bp.route('/company_profile/<string:id>/')
def company_profile(id):

    company = Company()
    query = company.query_company(id=id)
    return render_template('company_profile.html',
                           comp=query
                           )

@company_bp.route('/edit/<string:id>/', methods=['GET', 'POST'])
def edit(id):

    company = Company()
    query = company.query_company(id=id)
    if request.method != 'GET':
        company.update_comp(id=id, data=request.form)
        return redirect(url_for('company.company_profile', id=id))

    return render_template('company_edit.html',
                           comp=query
                           )
