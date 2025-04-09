from app.handlers.auth_handler import router as auth_router
from app.handlers.image_handler import router as image_router


routes = [
    auth_router,
    image_router
]

__all__ = [
    "routes",
]
