from singer_sdk.authenticators import SimpleAuthenticator


class RestTemplateAuthenticator(SimpleAuthenticator):

    @classmethod
    def create_for_stream(cls, stream) -> "RestTemplateAuthenticator":
        from tap_rest_template.secret import Secret
        return cls(
            stream=stream,
            auth_headers={'customer-key': Secret().get_secrets('singer', 'test')['customer-key']}
        )
