from .blueprints import image_editor_bp
from flask import render_template, request, url_for
from config import Config
from PIL import Image
from .exeptions import BadCoordinates
from profapp.models.files import File, FileContent
from db_init import db_session
from io import BytesIO
from time import gmtime, strftime
from .views_filemanager import file_query
import sys

@image_editor_bp.route('/<string:img_id>/<string:new_name>', methods=['GET', 'POST'])
def image_editor(img_id, new_name):

    ratio = Config.IMAGE_EDITOR_RATIO
    height = Config.HEIGHT_IMAGE
    thumbnail = File()
    thumbnail_content = FileContent()
    size = (int(ratio*height), height)
    image_id = img_id

    if request.method != 'GET':
        print(request.json)
        image_query = file_query(image_id, File)
        image_content = db_session.query(FileContent).filter_by(id=image_id).first()
        image = Image.open(BytesIO(image_content.content))
        area = [int(y) for x, y in sorted(zip(request.form.keys(), request.form.values()))
                if int(y) >= 0 and int(y) <= max(image.size) and x != "5rotate"]
        if area:
            angle = int(request.form["5rotate"])*-1
            area[2] = (area[0]+area[2])
            area[3] = (area[1]+area[3])
            rotated = image.rotate(angle)
            cropped = rotated.crop(area).resize(size)

            bytes_file = BytesIO()
            cropped.save(bytes_file, image_query.mime.split('/')[-1].upper())
            thumbnail.md_tm = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            thumbnail.size = sys.getsizeof(bytes_file.getvalue())
            thumbnail.name = new_name+'.'+image_query.name.split('.')[-1]
            thumbnail.mime = image_query.mime
            db_session.add(thumbnail)
            db_session.commit()
            thumbnail_content.content = bytes_file.getvalue()
            thumbnail_content.id = thumbnail.id
            db_session.add(thumbnail_content)
            db_session.commit()
            image_id = thumbnail.id

        else:
            db_session.rollback()
            raise BadCoordinates

    return render_template('image_editor.html',
                           ratio=ratio,
                           img_id=img_id,
                           new_name=new_name,
                           image=url_for('filemanager.get', id=image_id)
                           )
