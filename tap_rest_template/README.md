# tap-rest-template

`tap-rest-template` is a Singer Tap for SSP. It is assumed SSP will primarily use this target in association with the aws s3 tap though not required.

This was built using the [SSP Tap REST Template](https://github.com/sixthst/tap-rest-template). That was extended for SSP from the [Meltano Target SDK](https://sdk.meltano.com).

## Installation

Install with command `meltano install`. Assumes ssp-github is part of your .ssh/config.

```yml
  loaders:
  - name: tap-rest-template
    namespace: tap_rest_template
    pip_url: git+ssh://ssp-github/sixthst/tap-rest-template.git
    executable: tap-rest-template
```

## Configuration

### Accepted Config Options

- name: host
    kind: password
- name: rest_resource_version: Rest resource version from the URI
    kind: password
- name: exclude_stream_csv: Optional CSV to exclude streams i.e. Exclude resource not supported by REST_RESOURCE_VERSION
    kine: password
- name: include_stream_csv: Optional CSV to include streams
    kine: password
- name: remote_flag: an optional flag to ssh tunnel into the server
    kind: boolean
- name: debug_flag: an optional flag to send more information to `self.logger.info`
    kind: boolean

***Note: When the remote_flag is set to true it assumes that the remote machine can ssh to the singer runtime machine using the srvc_singer user via a SSH host config entry name of `singer-srvc`***

A full list of supported settings and capabilities for this
target is available when installed by running:

```bash
tap-rest-template --about
```

A JSON dictionary is stored for each resource in `tap_rest_template/resources/`.  The resource dictionary is used by the tap to do the following:

- validate the schema from the source system
- validate the data type from the source system
- facilitate serializing the data to JSON singer format

### Tap Authentication and Authorization

The tap uses the SDK `SimpleAuthenticator` and the class `Secret` to get the secrets from AWS Secret Manager and pass it to the REST API through the header.  Secrets are looked up by the key `{environment}/{app}/api`. The runtime uses the following environment variables at runtime to look get the secret:

- ADMIN_AWS_ACCESS_KEY_ID
- ADMIN_AWS_SECRET_ACCESS_KEY

## Tap Capabilities

### TapRestTemplate Class

- Extends Meltano SDK class `Tap` to validate the config
- Discover streams imported by the TapRestTemplateStream class
  - Filter Streams via `stream_filter_csv`
    - Filter out Streams that are not compatible with `rest_resource_version`
    - Filter out Streams that are not wanted for the data movement

### TapRestTemplateStream Class

Extends the Meltano SDK class `RESTStream` to do the following:

- Manage streams from the `tap_rest_template/resources` folder
  - Discovery
  - Stream validation
- Parse records from the rest endpoint
  - Flatten dictionary records to the reference `Name` item
- Authenticate using the Meltano SDK RestTemplateAuthenticator
- Get the URL used for look up
  - Establish SSH tunnel if remote

### RestTemplateAuthenticator Class

- Extend Meltano `SimpleAuthenticator` class for authorization
- Get secret from `Secret` class
- Facilitate authentication via header dictionary

### Secret Class

- Get secret from AWS secret manager

## Extending Streams

- Add new resources to the `tap_rest_template/resources` folder
- Add new resource class to the `tap_rest_template/streams.py` file.
- import above class to the `tap_rest_template/tap.py` file.
- add above class to the `STREAM_TYPES` list generator in the `tap_rest_template/tap.py` file.

sample resource class for the Template:

```python
class {NewResourceName}Stream(TapRestTemplateStream):
    name = '{NewResourceName}'
    path = '{NewResourceName}'
    primary_keys = ['{NewResourceName}ID']
    schema_filepath = SCHEMAS_DIR / '{NewResourceName}.json'
```

## Usage

You can run `tap-rest-template` by itself or in a pipeline using [Meltano](www.meltano.com).

```bash
tap-rest-template --version
tap-rest-template --help
meltano elt tap-rest-template target-jsonl
```
