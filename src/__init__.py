from flask import Flask

from config import configs

def create_app(testing=False):
    app = Flask(__name__)

    if testing:
        app.config.from_object(configs['testing'])
    else:
        app.config.from_object(configs[app.env])

    from . import view
    app.register_blueprint(view.bp)

    return app
