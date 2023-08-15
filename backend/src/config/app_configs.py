from typing import Any, List, Dict
from pydantic import BaseSettings
from src.constants import Environment


class Setting(BaseSettings):
    ENVIRONMENT: Environment = Environment.TESTING
    APP_VERSION: str = "0.0.1"
    DATABASE_URL: str
    CORS_ORIGINS: List[str]
    CORS_HEADERS: List[str]

    class Config:
        # `.env.prod` takes priority over `.env`
        env_file = ".env", ".env.prod"


settings = Setting()

app_configs: Dict[str, Any] = {
    "title": "Delus first web app",
    "version": "0.0.1",
    "contact": {
        "name": "Duy Bui",
        "url": "https://delusthefirst.tech",
        "email": "kid21200@gmail.com",
    },
    "license_info": {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
}
