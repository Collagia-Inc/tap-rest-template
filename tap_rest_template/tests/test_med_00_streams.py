from requests.models import Response
from tap_rest_template.tests.configurations.fixtures_streams import (rest_template_stream_class, mock_content,
                                                                     mock_subprocess_response)
from tap_rest_template.tests.configurations.fixtures_tap import (tap_rest_template_class, tap_config_stream_v2,
                                                                 tap_config_good)
from pytest import raises
import requests_mock


def mock_request():
    from requests import get
    return get('http://test.com')


def test_stream_flatten(tap_rest_template_class, rest_template_stream_class, tap_config_stream_v2, mock_content):
    with requests_mock.Mocker() as mock:
        mock.get('http://test.com', status_code=200, content=mock_content)
        tap_obj = tap_rest_template_class(tap_config_stream_v2)
        mock_response = mock_request()
        stream_obj = rest_template_stream_class(tap=tap_obj, schema='tap_rest_template/resources/Test.json',
                                                name='Test')
        stream_obj.url_base
        parse_response = stream_obj.parse_response(mock_response)
        for row in parse_response:
            assert row['Nested'] == 'ABC'


def test_stream_subprocess_error(mocker, tap_rest_template_class, rest_template_stream_class, tap_config_good,
                                 mock_subprocess_response):
    tap_obj = tap_rest_template_class(tap_config_good)
    stream_obj = rest_template_stream_class(tap=tap_obj, schema='tap_rest_template/resources/Test.json', name='Test')
    mocker.patch.object(stream_obj, '_exe_ssh_process', return_value=mock_subprocess_response)
    with raises(Exception) as error_obj:
        stream_obj.url_base
    v_error_msg = 'SSH Error! Check your .ssh/config\nCommand: test command\nError: test stderr\nOutput: test stdout'
    assert str(error_obj.value) == v_error_msg
