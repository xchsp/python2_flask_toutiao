import os

flask_secret_key = "CHANGEME"

base = os.path.dirname(os.path.abspath(__file__))
image_upload_folder = os.path.join(base, 'images')
