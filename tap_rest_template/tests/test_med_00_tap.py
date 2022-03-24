from tap_rest_template.tests.configurations.fixtures_tap import tap_rest_template_class, tap_config_good
from pytest import raises


def tests_tap_with_good_config(tap_rest_template_class, tap_config_good):
    assert tap_rest_template_class(tap_config_good)


def tests_tap_with_good_config_no_exclude(tap_rest_template_class, tap_config_good):
    del tap_config_good['exclude_stream_csv']
    assert tap_rest_template_class(tap_config_good)


def tests_tap_with_good_config_no_include(tap_rest_template_class, tap_config_good):
    del tap_config_good['include_stream_csv']
    assert tap_rest_template_class(tap_config_good)
