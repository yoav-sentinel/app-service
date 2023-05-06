from marshmallow import Schema, fields

from models.app import AppStatus


class AppIdPathSchema(Schema):
    app_id = fields.Integer(required=True)


class PostAppSchema(Schema):
    developer_id = fields.Integer(required=True)
    app_name = fields.String(required=True)


class AppsFilterSchema(Schema):
    developer_id = fields.Integer()
    app_name = fields.Integer()
    app_status = fields.Enum(AppStatus)


class AppResponseSchema(Schema):
    app_id = fields.Integer(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
    developer_id = fields.Integer(required=True)
    app_name = fields.String(required=True)
    app_status = fields.Enum(AppStatus, required=True)


class AppsResponseSchema(Schema):
    apps = fields.List(fields.Nested(AppResponseSchema(many=True)))


class UploadAppFileResponseSchema(Schema):
    result = fields.String(required=True)
    task_id = fields.String(required=True)


class DeleteAppResponseSchema(Schema):
    result = fields.String(required=True)
