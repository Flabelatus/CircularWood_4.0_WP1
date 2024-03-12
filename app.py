import os
import datetime

from datetime import timedelta, timezone
from flask import Flask, jsonify, request, Response
from flask_jwt_extended import JWTManager, get_jwt, get_jwt_identity, set_access_cookies, create_access_token
from flask_migrate import Migrate
from flask_smorest import Api
from flask_cors import CORS
from load_dotenv import load_dotenv

from db import db
from resources.production import production_blp
from resources.wood import blp as wood_blueprint
from resources.tagslist import blp as tags_blueprint
from resources.design_requirements import design_blp
from resources.user import user_blp
from resources.history import history_blp
from resources.point_cloud import pointcloud_blp
from resources.impact import impact_blp
from blocklist import BLOCKLIST


def create_app(db_url=None):
    app = Flask(__name__)

    load_dotenv()
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['API_TITLE'] = "Wood Database REST API"
    app.config['API_VERSION'] = "v1.1"
    app.config['OPENAPI_VERSION'] = '3.0.3'
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/api-docs"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config["JWT_COOKIE_SECURE"] = False
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config['JWT_COOKIE_SAMESITE'] = 'Strict'
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_CSRF_IN_COOKIES"] = True

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///instance/data.db"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "ROBOT-LAB_118944794548470618589981863246285508728"
    jwt = JWTManager(app)

    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.datetime.now(timezone.utc)
            target_timestamp = datetime.datetime.timestamp(
                now + timedelta(minutes=10))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT. Just return the original response
            return response

    cors = CORS(
        app,
        origins=["https://robotlab-db-gui.onrender.com",
                 "http://localhost:3000"],
        allow_headers=[
            "Accept", "Content-Type", "X-Auth-Email", "X-Auth-Key", "X-CSRF-Token", "Origin", "X-Requested-With",
            "Authorization"
        ]
    )

    @app.after_request
    def creds(response):
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            res = Response()
            res.headers['X-Content-Type-Options'] = '*'
            return res

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "the token is not fresh",
                    "error": "fresh_token_required"
                }
            ), 401
        )

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        """
        The function to get the `jti` from the JWT in the Blocklist
        :param jwt_header: The header from the JWT to be used in case of need
        :param jwt_payload: The JWT payload to check for `jti`
        :return: The `jti` of the JWT from the blocklist.
        """
        return jwt_payload['jti'] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "the token has been revoked.",
                    "error": "token_revoked"
                }
            ), 401
        )

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # Not the best way I know, but for now it works, later user modes need to be create as well.
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "message": "the token has expired.",
                    "error": "token_expired"
                }
            ), 401
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {
                    "message": "signature verification failed.",
                    "error": "invalid_token"
                }
            ), 401
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "message": "request does not contain a valid access token.",
                    "error": "authorization_required"
                }
            ), 401
        )

    @app.before_first_request
    def create_tables():
        db.create_all()

    api.register_blueprint(wood_blueprint)
    api.register_blueprint(tags_blueprint)
    api.register_blueprint(design_blp)
    api.register_blueprint(user_blp)
    api.register_blueprint(production_blp)
    api.register_blueprint(history_blp)
    api.register_blueprint(pointcloud_blp)
    api.register_blueprint(impact_blp)

    return app
