from pytest import fixture
from os import environ


# this represents a valid meltano.yml config
@fixture(scope="module")
def tap_config_good():
    return {
        'host': 'test.host.com',
        'rest_resource_version': 'v2',
        'exclude_stream_csv': 'Test, Employees',
        'include_stream_csv': 'Test',
        'remote_flag': True,
        'debug_flag': True}


@fixture(scope="module")
def tap_config_stream_v2():
    return {
        'host': 'test.host.com',
        'rest_resource_version': 'v2',
        'include_stream_csv': 'Test',
        'debug_flag': True}


@fixture(scope="module")
def tap_rest_template_class():
    from tap_rest_template.tap import TapRestTemplate
    return TapRestTemplate
