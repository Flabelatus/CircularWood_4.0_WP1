from flask.views import MethodView
from flask_smorest import abort, Blueprint
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import DesignRequirements
from schema import DesignRequirements

design_blp = Blueprint(
    'Design Requirements',
    'requirements',
    description='Operations on the requirements'
)


@design_blp.route("/requirements")
class DesignRequirements(MethodView):
    # Get all method
    # Post method
    pass


@design_blp.route("/requirement/<int:requirement_id>")
class DesignRequirementByID(MethodView):
    # Get by ID
    # Delete
    pass
