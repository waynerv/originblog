import http

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from httpx import HTTPError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from app.utils.exception import CustomError


def register_error_handlers(app):
    @app.exception_handler(StarletteHTTPException)
    def handle_http_error(request, exc) -> JSONResponse:
        """
        Handle HTTPExceptions.

        Include the error description and corresponding status code.
        """
        content = {
            'type': http.HTTPStatus(exc.status_code).phrase,
            'message': exc.detail if exc.detail else http.HTTPStatus(exc.status_code).description,
            'status': exc.status_code,
            'detail': None
        }
        return JSONResponse(content, status_code=exc.status_code)

    @app.exception_handler(HTTPError)
    def handle_httpx_response_error(request, exc) -> JSONResponse:
        """
        Handle httpx response HTTPExceptions.

        Include the error description and corresponding status code.
        """
        # reraise exceptions like ConnectTimeout...
        if exc.response is None:
            raise exc

        json_data = exc.response.json()
        content = {
            'type': json_data['type'] if json_data and json_data.get('type') else http.HTTPStatus(
                exc.response.status_code).phrase,
            'message': json_data['message'] if json_data and json_data.get('message') else http.HTTPStatus(
                exc.response.status_code).description,
            'status': exc.response.status_code,
            'detail': str(exc)
        }
        return JSONResponse(content, status_code=exc.response.status_code)

    @app.exception_handler(RequestValidationError)
    def handle_validation_error(request, exc) -> JSONResponse:
        """
        Handle pydantic parser errors.

        Ensures a JSON response including all error messages produced from the
        parser, that we know to be available on the error object.
        """
        content = {
            'type': 'ValidationError',
            'message': '请求数据不合法',
            'status': 422,
            'detail': jsonable_encoder(exc.errors())
        }
        return JSONResponse(content, status_code=422)

    @app.exception_handler(CustomError)
    def handle_custom_error(request, exc) -> JSONResponse:
        """
        Handle custom errors.

        Ensures a JSON response including all error messages produced from raised exceptions.
        """
        content = exc.to_dict()
        return JSONResponse(content, status_code=exc.status_code)
