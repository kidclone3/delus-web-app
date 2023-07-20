from typing import Any
from pydantic import BaseSettings
from src.constants import Environment


class Setting(BaseSettings):
    ENVIRONMENT: Environment = Environment.TESTING
    APP_VERSION: str = "0.0.1"

    CORS_ORIGINS: list[str]
    CORS_HEADERS: list[str]

    class Config:
        # `.env.prod` takes priority over `.env`
        env_file = ".env", ".env.prod"


settings = Setting()

app_configs: dict[str, Any] = {
    "title": "Delus first web app",
    "version": "0.0.1",
    "contact": {
        "name": "Duy Bui",
        "url": "https://delusthefirst.tech",
        "email": "kid21200@gmail.com",
    },
    "license_info": {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    },
}
