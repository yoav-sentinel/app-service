from functools import wraps

from flask import request, jsonify
from marshmallow import ValidationError


def api_endpoint(url, methods, query_schema=None, payload_schema=None, path_schema=None, response_schema=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if path_schema:
                try:
                    # Load the path schema class and validate path parameters
                    path_schema().load(kwargs)
                except ValidationError as err:
                    return jsonify({"error": err.messages}), 400
            if query_schema:
                try:
                    # Load the query schema class and validate query string parameters
                    query_schema().load(request.args)
                except ValidationError as err:
                    return jsonify({"error": err.messages}), 400

            if payload_schema:
                try:
                    # Load the payload schema class and validate JSON payload
                    payload_schema().load(request.get_json())
                except ValidationError as err:
                    return jsonify({"error": err.messages}), 400

            # Call the API endpoint function and get the response
            response = f(*args, **kwargs)

            if response_schema:
                try:
                    # Load the response schema class and validate the response
                    response_data = response.get_json()
                    response_schema().load(response_data)
                except ValidationError as err:
                    return jsonify({"error": err.messages}), 500

            return response

        wrapper.__name__ = f.__name__
        wrapper.url = url
        wrapper.methods = methods
        return wrapper

    return decorator
