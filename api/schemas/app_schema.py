from marshmallow import Schema, fields, validate

from models.app import AppStatus


class AppIdPathSchema(Schema):
    app_id = fields.Integer(required=True)


class PostAppSchema(Schema):
    developer_id = fields.Integer(required=True)
    app_name = fields.String(required=True)


class AppsFilterSchema(Schema):
    developer_id = fields.Integer()
    app_name = fields.String()
    app_status = fields.String(validate=validate.OneOf(AppStatus.app_status_values()))


class AppResponseSchema(Schema):
    app_id = fields.Integer(required=True, attribute='id')
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
    developer_id = fields.Integer(required=True)
    app_name = fields.String(required=True)
    app_status = fields.String(required=True, validate=validate.OneOf(AppStatus.app_status_values()))


class AppsResponseSchema(Schema):
    apps = fields.List(fields.Nested(AppResponseSchema()))


class UploadAppFileResponseSchema(Schema):
    result = fields.String(required=True)
    task_id = fields.String(required=True)


class DeleteAppResponseSchema(Schema):
    result = fields.String(required=True)
