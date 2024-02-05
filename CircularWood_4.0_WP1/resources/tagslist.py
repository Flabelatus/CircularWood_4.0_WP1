from db import db
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from models import WoodModel, TagModel, WoodTagsModel
from schema import TagSchema, TagAndWoodSchema, TagUpdateSchema
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint('Tags', 'tags', description='Operations on tags')


@blp.route("/tags")
class TagsList(MethodView):

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, parsed_data):
        if TagModel.query.filter(TagModel.name == parsed_data['name']).first():
            abort(400, message='This tag exists already')

        tag = TagModel(**parsed_data)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag

    @blp.response(200, TagSchema(many=True))
    def get(self):
        tag = TagModel.query.all()
        return tag


@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):

    @blp.response(200, TagSchema)
    def get(self, tag_id):
        return TagModel.query.get_or_404(tag_id)

    @blp.arguments(TagUpdateSchema)
    @blp.response(200, TagUpdateSchema)
    def patch(self, parsed_data, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        if tag:
            tag.name = parsed_data['name']
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return tag

    @blp.response(200, TagSchema)
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        db.session.delete(tag)

        db.session.commit()

        return {
            'message': "The tag removed"
        }


@blp.route("/wood/<int:wood_id>/tag/<int:tag_id>")
class LinkTagsToWood(MethodView):

    @blp.response(201, TagAndWoodSchema)
    def post(self, wood_id, tag_id):
        wood = WoodModel.query.get_or_404(wood_id)
        tag = TagModel.query.get_or_404(tag_id)
        wood.tags.append(tag)
        try:
            db.session.add(wood)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return {
            "tag": tag,
            "wood": wood
        }

    @blp.response(200, TagAndWoodSchema)
    def delete(self, wood_id, tag_id):
        wood = WoodModel.query.get_or_404(wood_id)
        tag = TagModel.query.get_or_404(tag_id)

        wood.tags.remove(tag)
        try:
            db.session.add(wood)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return {
            'message': "Wood removed from tag",
            "wood": wood,
            "tag": tag
        }


@blp.route('/woods_tags/<int:woods_tag_id>')
class WoodsTagsByID(MethodView):
    @blp.response(200, TagSchema)
    def get(self, woods_tag_id):
        wood_tag = WoodTagsModel.query.get_or_404(woods_tag_id)
        return wood_tag


@blp.route('/woods_tags/tag/<int:tag_id>')
class WoodByTag(MethodView):

    @blp.response(200, TagSchema(many=True))
    def get(self, tag_id):
        wood_tags_id = WoodTagsModel.query.filter(WoodTagsModel.tag_id == tag_id).all()
        return wood_tags_id


@blp.route('/tag/<string:tag_name>')
class TagByName(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_name):
        tag = TagModel.query.filter_by(name=tag_name).first()
        return tag


@blp.route('/wood/tag/<string:tag_name>')
class WoodByTagName(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, tag_name):
        tag = TagModel.query.filter_by(name=tag_name).first()
        tag_id = tag.id
        woods_tags = WoodTagsModel.query.filter(WoodTagsModel.tag_id == tag_id).all()

        wood_ids = [tag.wood_id for tag in woods_tags]
        woods = [WoodModel.query.filter_by(id=_id).first() for _id in wood_ids]

        return woods

