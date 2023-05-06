# import re
#
# from marshmallow import fields
#
#
# class CamelCaseMixin:
#     def _serialize(self, value, attr, obj, **kwargs):
#         camel_attr = snake_to_camel(attr)
#         return super(CamelCaseMixin, self)._serialize(value, camel_attr, obj, **kwargs)
#
#     def _deserialize(self, value, attr, data, **kwargs):
#         attr = camel_to_snake(attr)
#         return super(CamelCaseMixin, self)._deserialize(value, attr, data, **kwargs)
#
#
# class ApiField:
#     class Field(CamelCaseMixin, fields.Field):
#         pass
#
#     class Integer(CamelCaseMixin, fields.Integer):
#         pass
#
#     class String(CamelCaseMixin, fields.String):
#         pass
#
#     class DateTime(CamelCaseMixin, fields.DateTime):
#         pass
#
#     class Enum(CamelCaseMixin, fields.Enum):
#         pass
#
#     class List(CamelCaseMixin, fields.List):
#         pass
#
#     class Nested(CamelCaseMixin, fields.Nested):
#         pass
#
#
# def camel_to_snake(name):
#     """
#     Converts a string from camelCase format to snake_case format.
#     :param name: String in camelCase format
#     :return: String in snake_case format
#     """
#     pattern = re.compile(r'(?<!^)(?=[A-Z])')
#     result = pattern.sub('_', name).lower()
#     return result
#
#
# def snake_to_camel(name):
#     """
#     Converts a string from snake_case format to camelCase format.
#     :param name: String in snake_case format
#     :return: String in camelCase format
#     """
#     components = name.split('_')
#     return components[0] + ''.join(x.title() for x in components[1:])
