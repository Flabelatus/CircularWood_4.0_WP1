import os
import datetime

from datetime import timedelta

from flask import Flask, jsonify, request, Response
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_smorest import Api
from flask_cors import CORS
from load_dotenv import load_dotenv
from flask_uploads import configure_uploads
from apscheduler.schedulers.background import BackgroundScheduler

from db import db
from workflow.api_client.modify_wood_rows import get_modifiable_fields
from settings import app_settings, logger
from models import WoodModel
from blocklist import BLOCKLIST
from utils.image_helpers import IMAGE_SET

# Api resources
from resources.production import production_blp
from resources.wood import blp as wood_blueprint
from resources.tagslist import blp as tags_blueprint
from resources.design_requirements import design_blp
from resources.user import user_blp
from resources.history import history_blp
from resources.point_cloud import pointcloud_blp
from resources.impact import impact_blp
from resources.sub_wood import sub_wood_blp
from resources.image import image_blueprint


def create_app(db_url=None):
    load_dotenv()

    # ================ Creation of the Application ================
    app = Flask(__name__)

    # ================ Application configurations ================

    if app_settings is not None:

        app.config['API_TITLE'] = app_settings.api_info['title']
        app.config['API_VERSION'] = app_settings.api_info['version']
        app.config["SECRET_KEY"] = os.urandom(24)
        app.config['PROPAGATE_EXCEPTIONS'] = app_settings.api_configs['propogate_exceptions']
        app.config['OPENAPI_VERSION'] = app_settings.doc_configs['service']['openapi_version']
        app.config["OPENAPI_URL_PREFIX"] = app_settings.doc_configs['service']['openapi_url_prefix']
        app.config["OPENAPI_SWAGGER_UI_PATH"] = app_settings.doc_configs['service']['openapi_swagger_ui_path']
        app.config["OPENAPI_SWAGGER_UI_URL"] = app_settings.doc_configs['service']['openapi_swagger_ui_url']
        # app.config["JWT_COOKIE_SECURE"] = False
        # app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
        # app.config['JWT_COOKIE_SAMESITE'] = 'Strict'
        # app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
        app.config["JWT_CSRF_IN_COOKIES"] = app_settings.security_configs['cookie_settings']['csrf_in_cookies']
        app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET", os.urandom(24))
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv(
            "DATABASE_URL", "sqlite:///instance/data.db")
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = app_settings.db_configs['track_modifications']
        app.config['UPLOADED_IMAGES_DEST'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'img')
        app.config['MAX_CONTENT_LENGTH'] = app_settings.api_configs['max_content_length']
        app.config['CORS_HEADERS'] = app_settings.api_configs['cors']['allow_headers']

        logger.getChild("app")
        
        # logger.debug("\n")
        logger.info(f"API_TITLE: {app_settings.api_info['title']}")
        logger.info(f"API_VERSION: {app_settings.api_info['version']}")

        if app_settings.environment == 'development':
            logger.debug(f"JWT issuer: {app_settings.backend_env['url']}")
            logger.debug(f"ENVIRONMENT: {app_settings.environment}")    
            logger.debug(f"BACKEND_URL: {app_settings.backend_env['url']}")   
            logger.debug(f"PROPAGATE_EXCEPTIONS: {app_settings.api_configs['propogate_exceptions']}")  
        else:
            logger.info(f"JWT issuer: {app_settings.backend_env['url']}")
            logger.info(f"ENVIRONMENT: {app_settings.environment}")    
            logger.info(f"BACKEND_URL: {app_settings.backend_env['url']}")   
            logger.info(f"PROPAGATE_EXCEPTIONS: {app_settings.api_configs['propogate_exceptions']}")  

        logger.info(f"OPENAPI_VERSION: {app_settings.doc_configs['service']['openapi_version']}")  
        logger.info(f"MAX_CONTENT_LENGTH: {app_settings.api_configs['max_content_length']} (Bytes)")  

    # ================ Initialization of the App ================

    configure_uploads(app, IMAGE_SET)   # image upload config
    db.init_app(app)                    # database init
    # flask alembic init for database migrations
    migrate = Migrate(app, db)
    api = Api(app)                      # API init

    logger.info("Application initialized")  

    jwt = JWTManager(app)               # JWT init

    logger.info("JWT manager initialized")
    if app_settings.environment == 'development':
        logger.debug(f"JWT issuer: {app_settings.backend_env['url']}")
    else:
        logger.info(f"JWT issuer: {app_settings.backend_env['url']}")
    if not app_settings.security_configs['cookie_settings']['csrf_in_cookies']:
        logger.warning(f"JWT_CSRF_IN_COOKIES: {app_settings.security_configs['cookie_settings']['csrf_in_cookies']}")
    else:
        logger.info(f"JWT_CSRF_IN_COOKIES: {app_settings.security_configs['cookie_settings']['csrf_in_cookies']}")

    # @app.after_request
    # def refresh_expiring_jwts(response):
    #     try:
    #         exp_timestamp = get_jwt()["exp"]
    #         now = datetime.datetime.now(timezone.utc)
    #         target_timestamp = datetime.datetime.timestamp(
    #             now + timedelta(minutes=10))
    #         if target_timestamp > exp_timestamp:
    #             access_token = create_access_token(identity=get_jwt_identity())
    #             # set_access_cookies(response, access_token)
    #         return response
    #     except (RuntimeError, KeyError):
    #         # Case where there is not a valid JWT. Just return the original response
    #         return response

    # ================ CORS Middleware setup ================

    cors = CORS(
        app,
        origins=app_settings.api_configs['cors']['allowed_origins'],
        allow_headers=app_settings.api_configs['cors']['allow_headers']
    )

    if not app_settings.api_configs['cors']['access_control_allow_credentials']:
        logger.warning(f"CORS enabled: {app_settings.api_configs['cors']['access_control_allow_credentials']}\n")
    else:
        logger.info(f"CORS enabled: {True}\n")


    @app.after_request
    def creds(response):
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            res = Response()
            # Sends while card
            res.headers['X-Content-Type-Options'] = '*'
            return res

    # ================ Get some configuration parameters from the Application ================

    @app.route('/wood/modifiable-fields')
    def get_wood_model_modifiable_fields():
        
        modifiable_fields = get_modifiable_fields(WoodModel)
        return jsonify(modifiable_fields=modifiable_fields)

    # ================ JWT Claims ================

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        logger.error("the token is not fresh")
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
        logger.error("the token has been revoked.")
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
        logger.error("the token has expired.")
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
        logger.error("signature verification failed.")
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
        logger.error("request does not contain a valid access token.")
        return (
            jsonify(
                {
                    "message": "request does not contain a valid access token.",
                    "error": "authorization_required"
                }
            ), 401
        )

    # ================ Initialization of the Database tables ================

    @app.before_first_request
    def create_tables():
        db.create_all()

    # ================ Initialize the cron job for checking reservations ================

    def _get_expired_reservations():
        EXPIRY_TIME = 7  # 7 days for reservation
        now = datetime.datetime.now()
        woods = WoodModel.query.filter_by(reserved=True).all()
        expired_reservations = []

        for wood in woods:
            reservation_date = wood.reservation_time

            if isinstance(reservation_date, str):
                reservation_date = datetime.datetime.strptime(
                    reservation_date, "%Y-%m-%d")

            expiry_date = reservation_date + timedelta(days=EXPIRY_TIME)

            if now > expiry_date:
                expired_reservations.append(wood)
        
        logger.info(f"Retreived {len(expired_reservations)} expired wood reservations")
        
        return expired_reservations

    def check_and_update_reservations():
        with app.app_context():
            expired_woods = _get_expired_reservations()
            for wood in expired_woods:
                wood.reserved = False
                wood.reserved_at = ""
                wood.reserved_by = ""

                logger.info(f"Wood with ID: {wood.id}, came out of reservation")
                
                db.session.add(wood)

            db.session.commit()


    cron_job = BackgroundScheduler()
    cron_job.add_job(func=check_and_update_reservations,
                     trigger="interval", hours=1)
    cron_job.start()

    # ================ Registration of the API's resource blueprints ================

    api.register_blueprint(wood_blueprint)
    api.register_blueprint(tags_blueprint)
    api.register_blueprint(design_blp)
    api.register_blueprint(user_blp)
    api.register_blueprint(production_blp)
    api.register_blueprint(history_blp)
    api.register_blueprint(pointcloud_blp)
    api.register_blueprint(impact_blp)
    api.register_blueprint(sub_wood_blp)
    api.register_blueprint(image_blueprint)

    return app
