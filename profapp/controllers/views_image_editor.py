from .blueprints import image_editor_bp
from flask import render_template, request
from config import Config
from PIL import Image
from .exeptions import BadCoordinates
from profapp.models.files import File
from db_init import db_session
from io import BytesIO
from time import gmtime, strftime
from sqlalchemy.exc import DataError
import os
from stat import ST_SIZE

root = os.getcwd()+'/profapp/static/image_editor/tmp/'
@image_editor_bp.route('/<string:img_id>/<string:new_name>', methods=['GET', 'POST'])
def image_editor(img_id, new_name):
    ratio = Config.IMAGE_EDITOR_RATIO
    height = Config.HEIGHT_IMAGE
    image_id = img_id
    try:

        thumbnail = File()
        image_query = db_session.query(File).filter_by(id=img_id).first()
        image = Image.open(BytesIO(image_query.content))
        image.save(root+new_name, image_query.mime.split('/')[1].upper(), quality=75)
        size = (int(ratio*height), height)
        if request.method != 'GET':

            area = [int(y) for x, y in sorted(zip(request.form.keys(), request.form.values()))
                    if int(y) >= 0 and int(y) <= max(image.size)]
            if area:
                area[2] = (area[0]+area[2])
                area[3] = (area[1]+area[3])
                st = os.stat(root+new_name)
                image.crop(area)
                image.resize(size)
                thumbnail.md_tm = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                thumbnail.size = st[ST_SIZE]
                thumbnail.name = new_name+'.thumbnail'
                thumbnail.mime = 'thumbnail'
                db_session.add(thumbnail)
                db_session.commit()
                image_id = thumbnail.id

            else:
                raise BadCoordinates

    except BadCoordinates:
        print('Do somethink')
    except DataError:
        print('Bad id')

    return render_template('image_editor.html',
                           ratio=ratio,
                           image='image_editor/tmp/'+new_name,
                           img_id=image_id,
                           new_name=new_name
                           )
