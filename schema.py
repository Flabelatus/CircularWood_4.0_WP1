from marshmallow import fields, Schema


class WoodSchema(Schema):
    id = fields.Int(dump_only=True)
    length = fields.Float(required=True)
    width = fields.Float(required=True)
    height = fields.Float(required=True)
    weight = fields.Float(required=True)
    density = fields.Float(required=True)
    timestamp = fields.Str(required=True)
    color = fields.Str(required=True)
    reserved = fields.Bool()
    reservation_name = fields.Str()
    reservation_time = fields.Str()
    requirements = fields.Int()
    source = fields.Str()
    price = fields.Float()
    info = fields.Str()
    type = fields.Str()


class WasteWoodSchema(WoodSchema):
    contains_metal = fields.Bool(required=True)
    damaged = fields.Bool(required=True)
    stained = fields.Bool(required=True)


class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class TagUpdateSchema(Schema):
    name = fields.Str()


class TagSchema(PlainTagSchema):
    woods = fields.Nested(WoodSchema(), dump_only=True)


class TagAndWoodSchema(Schema):
    message = fields.Str()
    wood = fields.Nested(WoodSchema)
    tag = fields.Nested(TagSchema)

