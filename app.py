import os

from flask import Flask
from flask_migrate import Migrate
from flask_smorest import Api
from load_dotenv import load_dotenv

from db import db
from resources.wood import blp as wood_blueprint
from resources.tagslist import blp as tags_blueprint
from resources.design_requirements import design_blp


def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()

    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['API_TITLE'] = "Residual Wood REST API"
    app.config['API_VERSION'] = "v1"
    app.config['OPENAPI_VERSION'] = '3.0.3'
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    # @app.before_first_request
    # def create_tables():
    #     db.create_all()

    api.register_blueprint(wood_blueprint)
    api.register_blueprint(tags_blueprint)
    api.register_blueprint(design_blp)

    return app
