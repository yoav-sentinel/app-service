import http

from werkzeug.exceptions import NotFound as WerkzeugNotFound, BadRequest, InternalServerError


class ValidationError(Exception):
    pass


class NotFound(Exception):
    pass


class ServerError(Exception):
    pass


ERROR_STATUS_CODES = {
    BadRequest: http.HTTPStatus.BAD_REQUEST,
    ValidationError: http.HTTPStatus.BAD_REQUEST,

    NotFound: http.HTTPStatus.NOT_FOUND,
    WerkzeugNotFound: http.HTTPStatus.NOT_FOUND,

    ServerError: http.HTTPStatus.INTERNAL_SERVER_ERROR,
    InternalServerError: http.HTTPStatus.INTERNAL_SERVER_ERROR,
}
