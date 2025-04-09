import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware as FACORSMiddleware

logger = logging.getLogger(__name__)
default_value = ["*"]


def create_cors_middleware(
    origins: list[str] | None = None,
    methods: list[str] | None = None,
    headers: list[str] | None = None,
):
    return {
        "middleware": FACORSMiddleware,
        "params": {
            "allow_origins": origins or default_value,
            "allow_credentials": True,
            "allow_methods": methods or default_value,
            "allow_headers": headers or default_value,
        },
    }

def bind_exceptions(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def unhandled_error(request: Request, exc: Exception) -> JSONResponse:
        logger.exception(exc)
        response = JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Something went wrong"},
        )

        # Since the CORSMiddleware is not executed when an unhandled server exception
        # occurs, we need to manually set the CORS headers ourselves if we want the FE
        # to receive a proper JSON 500, opposed to a CORS error.
        # Setting CORS headers on server errors is a bit of a philosophical topic of
        # discussion in many frameworks, and it is currently not handled in FastAPI.
        # See dotnet core for a recent discussion, where ultimately it was
        # decided to return CORS headers on server failures:
        # https://github.com/dotnet/aspnetcore/issues/2378
        origin = request.headers.get('origin')

        if origin:
            cors_config = create_cors_middleware()

            # Have the middleware do the heavy lifting for us to parse
            # all the config, then update our response headers
            cors = cors_config["middleware"](
                app=app,
                **cors_config["params"],
            )

            response.headers.update(cors.simple_headers)

            # If request includes any cookie headers, then we must respond
            # with the specific origin instead of '*'.
            if cors.allow_all_origins:
                response.headers["Access-Control-Allow-Origin"] = origin
            # If we only allow specific origins, then we have to mirror back
            # the Origin header in the response.
            elif not cors.allow_all_origins and cors.is_allowed_origin(origin=origin):
                response.headers["Access-Control-Allow-Origin"] = origin
                response.headers.add_vary_header("Origin")

        return response
