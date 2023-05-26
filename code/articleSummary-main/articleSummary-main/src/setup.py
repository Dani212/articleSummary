from flask import Flask

UPLOAD_FOLDER = './new'


def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Register Blueprints
    from .blueprints.summary_route import sum_app
    app.register_blueprint(sum_app)

    return app
