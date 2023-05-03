import logging
import time
from functools import wraps

from flask import request, jsonify
from marshmallow import ValidationError

from config import LogLevel


def timer(logger=None, log_level=LogLevel.Info, threshold=0.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_cpu_time = time.process_time()
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            duration = end - start
            if duration >= threshold:
                if not logger:
                    func_logger = logging.getLogger('timer')
                else:
                    func_logger = logger
                getattr(func_logger, log_level.value)(
                    f"{func.__name__} took {duration:.4f} seconds. CPU time took {time.process_time() - start_cpu_time}")
            return result

        return wrapper

    return decorator


def api_endpoint(url, methods, query_schema=None, payload_schema=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if query_schema:
                try:
                    # Validate query string parameters
                    query_schema.load(request.args)
                except ValidationError as err:
                    return jsonify({"error": err.messages}), 400

            if payload_schema:
                try:
                    # Validate JSON payload
                    payload_schema.load(request.get_json())
                except ValidationError as err:
                    return jsonify({"error": err.messages}), 400

            return f(*args, **kwargs)

        wrapper.__name__ = f.__name__
        wrapper.url = url
        wrapper.methods = methods
        return wrapper

    return decorator
