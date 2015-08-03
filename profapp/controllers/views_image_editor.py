from .blueprints import image_editor_bp
from flask import render_template, request
from config import Config
from PIL import Image
from .exeptions import BadCoordinates
from profapp.models.files import File
from db_init import db_session
import os
from io import BytesIO

@image_editor_bp.route('/<string:img_id>/<string:new_name>', methods=['GET', 'POST'])
def image_editor(img_id, new_name):

    try:
        ratio = Config.IMAGE_EDITOR_RATIO
        height = Config.HEIGHT_IMAGE
        size = (int(ratio*height), height)
        if request.method != 'GET':
            image_to_crop = Image.open(get_image(img_id))
            area = [int(y) for x, y in sorted(zip(request.form.keys(), request.form.values()))
                    if int(y) >= 0 and int(y) <= max(image_to_crop.size)]
            if area:
                area[2] = (area[0]+area[2])
                area[3] = (area[1]+area[3])
                cropped = image_to_crop.crop(area)
                cropped.resize(size)
                cropped.show()
            else:
                raise BadCoordinates
    except BadCoordinates:
        print('Do somethink')

    image = '../static/image_editor/assets/img/picture.jpg'

    return render_template('image_editor.html',
                           ratio=ratio,
                           image=image,
                           img_id=img_id,
                           new_name=new_name
                           )

def get_image(img_id):

    tmp = os.getcwd()+'/profapp/static/image_editor/assets/img/picture-2.jpg'
    image = db_session.query(File).filter_by(id=img_id).first()

#    with open(tmp, 'w') as f:
 #       f.write(b'image.content'.decode())
   # with open(tmp) as f:
    #    data = f.read()
    with open(tmp) as f:
        io = BytesIO(image.content)
        im = Image.open(io)
        print(im.size)

    new_file = Image.open(os.getcwd()+'/profapp/static/image_editor/assets/img/picture.jpg')
    print(new_file)
    return new_file

def deleteContent(pfile):
    pfile.seek(0)
    pfile.truncate()