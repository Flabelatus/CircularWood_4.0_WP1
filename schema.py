from marshmallow import fields, Schema
from werkzeug.datastructures import FileStorage


class FileStorageField(fields.Field):
    default_error_messages = {
        "invalid": "Not a valid image."
    }

    def _deserialize(self, value, attr, data, **kwargs) -> FileStorage:
        if value is None:
            return None

        if not isinstance(value, FileStorage):
            self.fail("invalid")

        return value


class HistorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    event = fields.Str()
    created_at = fields.Str()
    success = fields.Bool()
    wood_id = fields.Int()
    requirement_id = fields.Int()


class WoodSchema(Schema):
    id = fields.Int(dump_only=True)
    # current_id = fields.Str()
    # subsequent_id = fields.Str()
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
    # price = fields.Float()
    info = fields.Str()
    type = fields.Str()
    image = fields.Str()
    has_metal = fields.Bool()
    metal_bbox_coords = fields.Str()
    intake_id = fields.Int()
    # project_label = fields.Str()
    paint = fields.Str()
    # project_type = fields.Str()
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
    woods = fields.List(fields.Nested(
        WoodSchema(), dump_only=True, load_instance=True))


class TagAndWoodSchema(Schema):
    message = fields.Str()
    # wood = fields.Nested(WoodSchema)
    tag = fields.Nested(TagSchema)


class PlainDesignRequirementSchema(Schema):
    id = fields.Int(dump_only=True)
    part_name = fields.Str()
    part_file_path = fields.Str()
    tag = fields.Str()
    part = fields.Int()
    created_at = fields.Str()
    # Foreign keys
    project_id = fields.Int()
    design_geometry_id = fields.Int()
    wood_id = fields.Int()


class DesignRequirementSchema(PlainDesignRequirementSchema):
    woods = fields.List(fields.Nested(
        WoodSchema(), dump_only=True), load_instance=False)


class DesignRequirementsAndWoodsSchema(Schema):
    message = fields.Str()
    wood = fields.Nested(WoodSchema(), load_instance=True)
    requirements = fields.Nested(DesignRequirementSchema(), load_instance=True)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    # This must stay load only, since we never want to return the password
    password = fields.Str(required=True, load_only=True)


class PlainProjectSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    created_at = fields.Str(dump_only=True)
    client = fields.Str()
    design_geometry_count = fields.Int()
    parts_count = fields.Int()
    

class PlainDesignGeometrySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    created_at = fields.Str(dump_only=True)
    type = fields.Str()
    file_path = fields.Str()
    project_id = fields.Int()


class DesignGeometrySchema(PlainDesignGeometrySchema):
    design_parts = fields.Nested(PlainDesignRequirementSchema(), load_instance=True)


class ProjectSchema(PlainProjectSchema):
    design_geometries = fields.Nested(PlainDesignGeometrySchema(), load_instance=True)


class ProductionSchema(Schema):
    id = fields.Int(dump_only=True)
    operation = fields.Str()
    instruction = fields.Str()
    instruction_type = fields.Str()
    timestamp = fields.Int()
    status = fields.Str()
    wood_id = fields.Int()
    sub_wood_id = fields.Int()
    offset = fields.Float()
    # wood = fields.Nested(WoodSchema(), load_instance=False)


class PointCloudSchema(Schema):
    id = fields.Int(dump_only=True)
    pcd = fields.Str()
    wood_id = fields.Int()


class ImpactSchema(Schema):
    id = fields.Int(dump_only=True)
    carbon_footprint = fields.Str()
    codename = fields.Str()
    eco_costs = fields.Str()
    process = fields.Str()
    eco_toxicity = fields.Str()
    footprint = fields.Str()
    resource_depletion = fields.Str()
    human_health = fields.Str()
    material = fields.Str()
    wood_id = fields.Int()


class PlainSubWoodSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    length = fields.Float()
    width = fields.Float()
    height = fields.Float()
    density = fields.Float()
    color = fields.Str()
    deleted = fields.Bool()
    deleted_by = fields.Str()
    deleted_at = fields.Str()
    project_label = fields.Str()
    source = fields.Str()
    info = fields.Str()
    type = fields.Str()
    wood_id = fields.Int()
    design_id = fields.Int()


class SubWoodSchema(PlainSubWoodSchema):
    design = fields.Nested(PlainDesignRequirementSchema(), load_instance=True)


class ImageSchema(Schema):
    image = FileStorageField()


class MeshSchema(Schema):
    mesh = FileStorageField()


class CadSchema(Schema):
    cad = FileStorageField()