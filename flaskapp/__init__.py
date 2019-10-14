import os
from flask import Flask
from . import db
from . import routes


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskapp.sqlite'),
        # BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        UPLOAD_FOLDER=os.path.join(os.getcwd(), 'uploads')
        # UPLOAD_FOLDER = '/home/valentyn/Dev/simple_python_web_app/uploads'
    )

    app.register_blueprint(routes.bp)
    app.add_url_rule('/', endpoint='index')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    
    return app