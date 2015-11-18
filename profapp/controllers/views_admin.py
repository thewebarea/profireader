from .blueprints_declaration import admin_bp
from flask import g, request, url_for, render_template, flash, current_app


@admin_bp.route('/unconfirmed')
def translations():
    return render_template('admin/translations.html')

