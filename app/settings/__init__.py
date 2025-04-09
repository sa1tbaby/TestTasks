from importlib import import_module
from os import environ

env = environ.get("ENV_TYPE", "local")
from app.settings.base_settings import BaseSettings

module = import_module(name=f"app.settings.{env}")
Settings = module.Settings
settings = Settings()
__all__ = [
    "BaseSettings",
    "Settings",
    "settings",
    "env"
]
