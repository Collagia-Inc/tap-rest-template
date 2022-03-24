class Secret(object):

    def __init__(self):
        from os import environ
        environ['AWS_ACCESS_KEY_ID'] = environ['ADMIN_AWS_ACCESS_KEY_ID']
        environ['AWS_SECRET_ACCESS_KEY'] = environ['ADMIN_AWS_SECRET_ACCESS_KEY']
        from boto3 import client
        self.client = client('secretsmanager', 'us-east-1')

    def _get_secret_id(self, p_name, p_component):
        from os import environ
        return '{}/{}/{}'.format(environ['ENV'].lower(), p_name.lower(), p_component.lower())

    def get_secrets(self, p_name, p_component):
        from json import loads
        v_response_dict = self.client.get_secret_value(SecretId=self._get_secret_id(p_name, p_component))
        return loads(v_response_dict['SecretString'])
