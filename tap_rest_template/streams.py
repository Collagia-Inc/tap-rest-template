from pathlib import Path
from singer_sdk.streams import RESTStream
from typing import List
from tap_rest_template.auth import RestTemplateAuthenticator
from typing import Iterable
from requests import Response


SCHEMAS_DIR = Path(__file__).parent / Path("./resources")


class TapRestTemplateStream(RESTStream):
    limit: int = 100
    expand: List[str] = []

    def _exe_ssh_process(self):
        from subprocess import Popen, PIPE
        v_command = 'ssh singer-srvc & exit'
        process_object = Popen(v_command, stdout=PIPE, stderr=PIPE, shell=True)
        v_stdout, v_stderr = process_object.communicate()
        process_object.wait()
        return {'returncode': process_object.returncode, 'stdout': v_stdout.decode('utf-8').strip(),
                'stderr': v_stderr.decode('utf-8').strip(), 'command': v_command}

    def _exe_ssh(self):
        result_dict = self._exe_ssh_process()
        if result_dict['returncode'] != 0:
            error_message = 'SSH Error! Check your .ssh/config\nCommand: {}\nError: {}\nOutput: {}'\
                .format(result_dict['command'], result_dict['stderr'], result_dict['stdout'])
            raise ValueError(error_message)

    def _flaten_item_value(self, p_item_value):
        if type(p_item_value) == dict:
            return p_item_value['Name']
        else:
            return p_item_value

    def _format_row(self, p_row):
        return {v_item_key: self._flaten_item_value(p_row[v_item_key]) for v_item_key in p_row}

    def _get_tunnel(self):
        from sshtunnel import SSHTunnelForwarder
        self._exe_ssh()
        return SSHTunnelForwarder('singer-srvc', remote_bind_address=(self.config.get('host'), 8080))

    def _url(self, p_tunnel_obj):
        if p_tunnel_obj is None:
            v_url = 'http://{}:8080/api/{}/'.format(self.config.get('host'),
                                                    self.config.get('rest_resource_version').lower())
        else:
            v_url = 'http://127.0.0.1:{}/api/{}/'.format(p_tunnel_obj.local_bind_port,
                                                         self.config.get('rest_resource_version').lower())
        return v_url

    @property
    def authenticator(self) -> RestTemplateAuthenticator:
        return RestTemplateAuthenticator.create_for_stream(self)

    def parse_response(self, response: Response) -> Iterable[dict]:
        resp_json = response.json()
        if self.config.get('rest_resource_version') == 'v2':
            for v_row in resp_json['Selected']:
                v_format_row = self._format_row(v_row)
                if self.config.get('debug_flag'):
                    self.logger.info('v_row: {}'.format(v_row))
                yield v_format_row
        elif self.config.get('rest_resource_version') == 'v1':
            for v_row in resp_json['Items']:
                v_format_row = self._format_row(v_row)
                if self.config.get('debug_flag'):
                    self.logger.info('v_row: {}'.format(v_row))
                yield v_format_row

    @property
    def url_base(self) -> str:
        if self.config.get('remote_flag'):
            v_tunnel_obj = self._get_tunnel()
            v_tunnel_obj.start()
            v_url = self._url(v_tunnel_obj)
        else:
            v_tunnel_obj = None
            v_url = self._url(v_tunnel_obj)
        return v_url


class TestStream(TapRestTemplateStream):
    name = 'Test'
    path = 'Test'
    primary_keys = ['TestID']
    schema_filepath = SCHEMAS_DIR / 'Test.json'
