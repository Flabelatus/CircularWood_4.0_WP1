from marshmallow import fields, Schema


class HistorySchema(Schema):
    id = fields.Int(dump_only=True)
    event = fields.Str()
    created_at = fields.Str()
    wood_id = fields.Int()


class WoodSchema(Schema):
    id = fields.Int(dump_only=True)
    current_id = fields.Str()
    subsequent_id = fields.Str()
    name = fields.Str()
    length = fields.Float()
    width = fields.Float()
    height = fields.Float()
    weight = fields.Float()
    density = fields.Float()
    timestamp = fields.Str()
    updated_at = fields.Str()
    color = fields.Str()
    reserved = fields.Bool()
    used = fields.Bool()
    used_by = fields.Str()
    deleted = fields.Bool()
    deleted_by = fields.Str()
    deleted_at = fields.Str()
    reservation_name = fields.Str()
    reservation_time = fields.Str()
    source = fields.Str()
    price = fields.Float()
    info = fields.Str()
    type = fields.Str()
    image = fields.Str()
    has_metal = fields.Bool()
    metal_bbox_coords = fields.Str()
    intake_id = fields.Int()
    project_label = fields.Str()
    paint = fields.Str()
    project_type = fields.Str()
    is_fire_treated = fields.Bool()
    is_straight = fields.Bool()
    is_planed = fields.Bool()
    storage_location = fields.Str()

    history = fields.List(fields.Nested(HistorySchema(), load_instance=True))


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
    part_index = fields.Int()
    features = fields.Str()
    tag = fields.Str()
    part = fields.Str()
    project_id = fields.Str()
    created_at = fields.Str()
    wood_id = fields.Int()


class DesignRequirementSchema(PlainDesignRequirementSchema):
    woods = fields.List(fields.Nested(WoodSchema(), dump_only=True), load_instance=True)


class DesignRequirementsAndWoodsSchema(Schema):
    message = fields.Str()
    wood = fields.Nested(WoodSchema(), load_instance=True)
    requirements = fields.Nested(DesignRequirementSchema(), load_instance=True)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    # This must stay load only, since we never want to return the password
    password = fields.Str(required=True, load_only=True)


class ProductionSchema(Schema):
    id = fields.Int(dump_only=True)
    operation = fields.Str()
    instruction = fields.Str()
    instruction_type = fields.Str()
    timestamp = fields.Int()
    status = fields.Str()
    wood_id = fields.Int()
    wood = fields.Nested(WoodSchema(), load_instance=True)
