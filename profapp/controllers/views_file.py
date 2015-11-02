from .blueprints import file_bp
from flask import request, make_response, send_file, g
from ..models.files import File, FileContent, ImageCroped
from io import BytesIO
from .errors import BadCoordinates
from PIL import Image
from time import gmtime, strftime
import sys
from ..models.articles import Article, ArticlePortal
from ..models.portal import CompanyPortal, PortalDivision, Portal
from config import Config
from utils.db_utils import db
from ..models.company import Company


@file_bp.route('<string:file_id>/')
def get(file_id):
    image_query = file_query(File, file_id)
    image_query_content = g.db.query(FileContent).filter_by(id=file_id).first()
    response = make_response()
    response.headers['Content-Type'] = image_query.mime
    response.headers['Content-Disposition'] = 'filename=%s' % \
                                              image_query.name
    return send_file(BytesIO(image_query_content.content),
                     mimetype=image_query.mime, as_attachment=False)


def file_query(table, file_id):
    query = g.db.query(table).filter_by(id=file_id).first()
    return query


def crop_image(image_id, coordinates, ratio=Config.IMAGE_EDITOR_RATIO,
               height=Config.HEIGHT_IMAGE):
    croped = File()
    size = (int(ratio*height), height)
    image_query = file_query(File, image_id)
    image = Image.open(BytesIO(image_query.file_content.content))
    company_owner = db(Company, journalist_folder_file_id=image_query.root_folder_id).one()
    area = [int(a) for a in (coordinates['x'], coordinates['y'], coordinates['width'],
                             coordinates['height'])
            if int(a) in range(0, max(image.size))]

    if area:
        angle = int(coordinates["rotate"])*-1
        area[2] = (area[0]+area[2])
        area[3] = (area[1]+area[3])
        rotated = image.rotate(angle)
        cropped = rotated.crop(area).resize(size)
        bytes_file = BytesIO()
        cropped.save(bytes_file, image_query.mime.split('/')[-1].upper())
        croped.md_tm = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        croped.size = sys.getsizeof(bytes_file.getvalue())
        croped.name = image_query.name + '_croped'
        croped.parent_id = company_owner.system_folder_file_id
        croped.root_folder_id = company_owner.system_folder_file_id
        croped.mime = image_query.mime
        croped.file_content = FileContent(content=bytes_file.getvalue())
        copy_original_image_to_system_folder = image_query.copy_file(
            parent_folder_id=company_owner.system_folder_file_id,
            root_folder_id=company_owner.system_folder_file_id)
        
        g.db.add(croped)
        g.db.commit()
        return croped.id

    else:
        g.db.rollback()
        raise BadCoordinates
