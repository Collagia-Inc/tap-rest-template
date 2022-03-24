from typing import List
from singer_sdk import typing as th
from singer_sdk import Tap
from tap_rest_template.streams import (
    TestStream,
)

PLUGIN_NAME = "tap-rest-template"
STREAM_TYPES = [
    TestStream,
]


class TapRestTemplate(Tap):
    name = "tap-rest-template"
    config_jsonschema = th.PropertiesList(
        th.Property("host", th.StringType),
        th.Property("rest_resource_version", th.StringType),
        th.Property("exclude_stream_csv", th.StringType),
        th.Property("include_stream_csv", th.StringType),
        th.Property("remote_flag", th.BooleanType),
        th.Property("debug_flag", th.BooleanType)
    ).to_dict()

    def discover_streams(self) -> List:
        try:
            exclude_list = self.config.get('exclude_stream_csv').split(',')
        except AttributeError:
            exclude_list = []
        try:
            include_list = self.config.get('include_stream_csv').split(',')
        except AttributeError:
            include_list = []
        if len(include_list) == 0:
            return [stream(tap=self) for stream in STREAM_TYPES if stream.name not in exclude_list]
        else:
            return [stream(tap=self) for stream in STREAM_TYPES if stream.name not in exclude_list and
                    stream.name in include_list]


cli = TapRestTemplate.cli
