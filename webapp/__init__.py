from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(the_config):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        the_config: the python path of the config object,
                     e.g. project.config.ProdConfig
    """
    app = Flask(__name__)
    app.config.from_object(the_config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .media import create_module as media_create_module
    from .main import create_module as main_create_module
    media_create_module(app)
    main_create_module(app)

    return app