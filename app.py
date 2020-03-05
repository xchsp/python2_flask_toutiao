from flask import Flask
from flask_cors import CORS

import config
from model import Category

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = config.flask_secret_key


from views.auth import *
from views.category import *
from views.errors import *
from views.posts import *
from views.upload import *


if __name__ == '__main__':
    # Category(name='java').save()
    # Category(name='css').save()
    # Category(name='python').save()
    app.run()