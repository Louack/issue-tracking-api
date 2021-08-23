from rest_framework.exceptions import APIException


class ObjectNotFound(APIException):
    status_code = 404


class BadRequest(APIException):
    status_code = 400
