import os
import uuid

from flask import request, jsonify, send_from_directory

import config
from app import app
from model import Cover

@app.route('/api/file/<filename>')
def get_img(filename):
    return send_from_directory(config.image_upload_folder,filename)


@app.route('/api/upload/',methods=['POST'])
def upload():
    image = request.files.get('file')
    if image:
        if not image.filename.endswith(tuple(['.jpg','.png','.mp4'])):
            return jsonify({'message':'error file format'}),409

        print(uuid.uuid4())

        filename = str(uuid.uuid4()).replace('-','') + '.' + image.filename.split('.')[-1]

        if not os.path.isdir(config.image_upload_folder):
            os.makedirs(config.image_upload_folder)

        image.save(os.path.join(config.image_upload_folder, filename))

        cover = Cover(
            url=filename
        ).save()

    return jsonify(cover.to_public_json())
