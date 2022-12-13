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


class WasteWoodSchema(WoodSchema):
    contains_metal = fields.Bool(required=True)
    damaged = fields.Bool(required=True)
    stained = fields.Bool(required=True)

