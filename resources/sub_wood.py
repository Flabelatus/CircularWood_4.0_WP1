import datetime

from typing import Union, List, Dict
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import SubWoodModel, UserModel
from schema import SubWoodSchema, PlainSubWoodSchema

sub_wood_blp = Blueprint(
    "Sub Wood Model",
    "sub_wood",
    description="Operations on the sub_wood resource"
)


@sub_wood_blp.route("/subwood")
class SubWoodList(MethodView):

    @sub_wood_blp.response(200, SubWoodSchema(many=True))
    def get(self) -> List[SubWoodModel]:
        return SubWoodModel.query.all()

    @sub_wood_blp.arguments(PlainSubWoodSchema)
    @sub_wood_blp.response(201, PlainSubWoodSchema)
    def post(self, parsed_data: Dict):
        subwood = SubWoodModel(**parsed_data)
        try:
            db.session.add(subwood)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            abort(500, message=str(err))
        return subwood


@sub_wood_blp.route("/subwood/<int:subwood_id>")
class SubWoodByID(MethodView):

    @sub_wood_blp.response(200, SubWoodSchema)
    def get(self, subwood_id: int):
        subwood = SubWoodModel.query.get_or_404(subwood_id)
        return subwood

    @jwt_required()
    @sub_wood_blp.arguments(PlainSubWoodSchema)
    @sub_wood_blp.response(200, PlainSubWoodSchema)
    def patch(self, parsed_data: Dict, subwood_id: int):
        subwood = SubWoodModel.query.get_or_404(subwood_id)
        if subwood:
            subwood.name = parsed_data.get("name", "")
            subwood.length = parsed_data.get("length", 0)
            subwood.width = parsed_data.get("width", 0)
            subwood.height = parsed_data.get("height", 0)
            subwood.density = parsed_data.get("density", 0)
            subwood.color = parsed_data.get("color", "")
            subwood.source = parsed_data.get("source", "")
            subwood.info = parsed_data.get("info", "")
            subwood.type = parsed_data.get("type", "")
        db.session.add(subwood)
        db.session.commit()

        return subwood

    @jwt_required()
    def delete(self, subwood_id: int):
        subwood = SubWoodModel.query.get_or_404(subwood_id)
        user = UserModel.query.get_or_404(get_jwt_identity())
        if subwood:
            subwood.deleted = True
            subwood.deleted_at = datetime.datetime.now().strftime(
                "%Y-%m-$d %H:%M:%S"
            )
            subwood.deleted_by = user.username
        db.session.add(subwood)
        db.session.commit()

        return {
            "message": "successfully deleted the subwood "
        }, 200


@sub_wood_blp.route("/subwood/wood/<int:wood_id>")
class SubWoodByWoodID(MethodView):

    @sub_wood_blp.response(200, SubWoodSchema)
    def get(self, wood_id: int) -> Union[SubWoodModel, None]:
        subwood = SubWoodModel.query.filter_by(wood_id=wood_id).first()
        if not subwood:
            abort(404, message="subwood not found with this wood id")
        return subwood

    @jwt_required()
    @sub_wood_blp.arguments(PlainSubWoodSchema)
    @sub_wood_blp.response(200, PlainSubWoodSchema)
    def patch(self, parsed_data: Dict, wood_id: int):
        subwood = SubWoodModel.query.filter_by(wood_id=wood_id).first()
        if not subwood:
            abort(404, message="subwood not found with this wood id")

        if subwood:
            subwood.name = parsed_data.get("name", "")
            subwood.length = parsed_data.get("length", 0)
            subwood.width = parsed_data.get("width", 0)
            subwood.height = parsed_data.get("height", 0)
            subwood.density = parsed_data.get("density", 0)
            subwood.color = parsed_data.get("color", "")
            subwood.source = parsed_data.get("source", "")
            subwood.info = parsed_data.get("info", "")
            subwood.type = parsed_data.get("type", "")
        db.session.add(subwood)
        db.session.commit()

        return subwood

    @jwt_required()
    def delete(self, wood_id: int):
        subwood = SubWoodModel.query.filter_by(wood_id=wood_id).first()
        user = UserModel.query.get_or_404(get_jwt_identity())

        if not subwood:
            abort(404, message="subwood not found with this wood id")

        if subwood:
            subwood.deleted = True
            subwood.deleted_at = datetime.datetime.now().strftime(
                "%Y-%m-$d %H:%M:%S"
            )
            subwood.deleted_by = user.username
        db.session.add(subwood)
        db.session.commit()

        return {
            "message": "successfully deleted the subwood "
        }, 200


@sub_wood_blp.route("/subwood/design/<int:design_id>")
class SubWoodByDesignID(MethodView):

    @sub_wood_blp.response(200, SubWoodSchema)
    def get(self, design_id: int) -> Union[SubWoodModel, None]:
        subwood = SubWoodModel.query.filter_by(design_id=design_id).first()
        if not subwood:
            abort(404, message="subwood not found with this design id")
        return subwood

    @jwt_required()
    @sub_wood_blp.arguments(PlainSubWoodSchema)
    @sub_wood_blp.response(200, PlainSubWoodSchema)
    def patch(self, parsed_data: Dict, design_id: int):
        subwood = SubWoodModel.query.filter_by(design_id=design_id).first()
        if not subwood:
            abort(404, message="subwood not found with this design id")
        if subwood:
            subwood.name = parsed_data.get("name", "")
            subwood.length = parsed_data.get("length", 0)
            subwood.width = parsed_data.get("width", 0)
            subwood.height = parsed_data.get("height", 0)
            subwood.density = parsed_data.get("density", 0)
            subwood.color = parsed_data.get("color", "")
            subwood.source = parsed_data.get("source", "")
            subwood.info = parsed_data.get("info", "")
            subwood.type = parsed_data.get("type", "")
        db.session.add(subwood)
        db.session.commit()

        return subwood

    @jwt_required()
    def delete(self, design_id: int):
        subwood = SubWoodModel.query.filter_by(design_id=design_id).first()
        user = UserModel.query.get_or_404(get_jwt_identity())

        if not subwood:
            abort(404, message="subwood not found with this wood id")

        if subwood:
            subwood.deleted = True
            subwood.deleted_at = datetime.datetime.now().strftime(
                "%Y-%m-$d %H:%M:%S"
            )
            subwood.deleted_by = user.username
        db.session.add(subwood)
        db.session.commit()

        return {
            "message": "successfully deleted the subwood "
        }, 200
