import flask
import http

class _HTTPError(Exception):
    status_code = 0
    def __init__(self, message: str):
        self.message = message
    
    def json_response(self):
        response = flask.jsonify({"message": self.message})
        response.status_code = self.status_code
        return response

class _ClientError(_HTTPError):
    def __init__(self, message):
        super().__init__(message)

class _ServerError(_HTTPError):
    def __init__(self, message):
        super().__init__(message)

class NotFoundError(_ClientError):
    status_code = http.HTTPStatus.NOT_FOUND
    def __init__(self, message):
        super().__init__(message)
    

class BadRequestError(_ClientError):
    status_code = http.HTTPStatus.BAD_REQUEST
    def __init__(self, message):
        super().__init__(message)


class StringQueryMissingError(BadRequestError):
    def __init__(self, required_field: str):
        message = f"'{required_field}' is a required field in string query."
        super().__init__(message)

class ResourceNotFoundError(_ClientError):
    def __init__(self, resource_name: str):
        message = f"{resource_name} not found."
        super().__init__(message)