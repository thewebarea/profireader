from .blueprints import image_editor_bp
from flask import render_template, request, flash, url_for, redirect
from config import Config
from PIL import Image

@image_editor_bp.route('/<int:img_id>/<string:new_name>', methods=['GET', 'POST'])
def image_editor(img_id, new_name):

    ratio = Config.IMAGE_EDITOR_RATIO
    height = Config.HEIGHT_IMAGE
    size = (int(ratio*height), height)
    if request.method != 'GET':
        image_to_crop = Image.open(get_image())
        area = [int(y) for x, y in sorted(zip(request.form.keys(), request.form.values()))
                if int(y) >= 0 and int(y) <= max(image_to_crop.size)]
        if area:
            area[2] = (area[0]+area[2])
            area[3] = (area[1]+area[3])
            cropped = image_to_crop.crop(area)
            cropped.resize(size)
            cropped.show()

    image = get_image().replace('/home/viktor/profireader/profapp', '..')


    return render_template('image_editor.html',
                           ratio=ratio,
                           image=image,
                           img_id=img_id,
                           new_name=new_name
                           )

def get_image():

    image = '/home/viktor/profireader/profapp/static/image_editor/assets/img/picture.jpg'
    return image
