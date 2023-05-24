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
    woods = fields.List(fields.Nested(WoodSchema(), dump_only=True, load_instance=True))


class TagAndWoodSchema(Schema):
    message = fields.Str()
    # wood = fields.Nested(WoodSchema)
    tag = fields.Nested(TagSchema)


class PlainDesignRequirementSchema(Schema):
    id = fields.Int(dump_only=True)
    part_index = fields.Str()
    length = fields.Str()
    width = fields.Str()
    height = fields.Str()
    tag = fields.Str()
    part = fields.Str()
    project_id = fields.Str()
    created_at = fields.Int()


class WoodUpdateSchema(Schema):
    length = fields.Float()
    width = fields.Float()
    height = fields.Float()
    weight = fields.Float()
    density = fields.Float()
    timestamp = fields.Str()
    color = fields.Str()
    reserved = fields.Bool()
    reservation_name = fields.Str()
    reservation_time = fields.Str()
    source = fields.Str()
    price = fields.Float()
    info = fields.Str()
    type = fields.Str()


class DesignRequirementSchema(PlainDesignRequirementSchema):
    woods = fields.Nested(WoodSchema(), dump_only=True, load_instance=True)


class DesignRequirementsAndWoodsSchema(Schema):
    message = fields.Str()
    wood = fields.Nested(WoodSchema(), load_instance=True)
    requirements = fields.Nested(DesignRequirementSchema(), load_instance=True)
