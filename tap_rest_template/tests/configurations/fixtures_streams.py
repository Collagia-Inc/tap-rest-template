from pytest import fixture
from os import environ


@fixture(scope="module")
def rest_template_stream_class():
    from tap_rest_template.streams import TapRestTemplateStream
    return TapRestTemplateStream


@fixture(scope="module")
def mock_content():
    return '''{
"Selected": [{
"Id": 1,
"Nested": {
    "Id": 1,
    "Name": "ABC"}}]}'''.encode('utf-8')


@fixture(scope="module")
def mock_subprocess_response():
    return {'returncode': -1, 'stdout': 'test stdout', 'stderr': 'test stderr',
            'command': 'test command'}
