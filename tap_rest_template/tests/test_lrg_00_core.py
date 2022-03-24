from singer_sdk.testing import get_standard_tap_tests
from tap_rest_template.tap import TapRestTemplate
from os import environ


SAMPLE_CONFIG = {
    "host": environ['HOST'],
    "rest_resource_version": environ['REST_RESOURCE_VERSION'],
    "exclude_stream_csv": environ['EXCLUDE_STREAM_CSV'],
    "debug_flag": True,
    "remote_flag": True
}


def test_standard_tap_tests():
    tests = get_standard_tap_tests(
        TapRestTemplate,
        config=SAMPLE_CONFIG
    )
    for test in tests:
        test()
