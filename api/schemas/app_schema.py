from marshmallow import Schema, fields


class UploadAppFileQueryStringSchema(Schema):
    appId = fields.String(required=True)
