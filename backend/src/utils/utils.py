from typing import Any
from pydantic import BaseModel
import orjson
from datetime import datetime
from zoneinfo import ZoneInfo


def convert_datetime_to_gmt(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


def orjson_dumps(v: Any) -> str:
    return orjson.dumps(v, option=orjson.OPT_INDENT_2)


class ORJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        allow_population_by_field_name = True
        json_encoders = {datetime: convert_datetime_to_gmt}
