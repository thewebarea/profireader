from .blueprints import file_bp
from flask import request, make_response, send_file, g
from ..models.files import File, FileContent
from io import BytesIO
from ..models.articles import Article, ArticlePortal
from ..models.portal import CompanyPortal, PortalDivision, Portal
from config import Config


@file_bp.route('<string:file_id>/')
def get(file_id):
    image_query = file_query(file_id, File)
    image_query_content = g.db.query(FileContent).filter_by(
        id=file_id).first()
    response = make_response()
    response.headers['Content-Type'] = image_query.mime
    response.headers['Content-Disposition'] = 'filename=%s' % \
                                              image_query.name
    return send_file(BytesIO(image_query_content.content),
                     mimetype=image_query.mime, as_attachment=False)


def file_query(file_id, table):
    query = g.db.query(table).filter_by(id=file_id).first()
    return query
