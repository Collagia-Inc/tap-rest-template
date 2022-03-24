# tap-rest-template

`tap-rest-template` is a Singer Tap for SSP. It is assumed SSP will primarily use this target in association with the aws s3 tap though not required.

This was extended from the [Meltano Target SDK](https://sdk.meltano.com).

See the [README](https://github.com/sixthst/tap-rest-template/blob/master/tap_rest_template/README.md) that is installed with the target

## Local Development Environment

Assumptions: python 3.8, poetry and pipx have been installed to manage virtual environments.

### Initial setup

```bash
poetry install
pipx install meltano
meltano install
export ENV=[environment]
export HOST=[host value]
export REST_RESOURCE_VERSION=[resource version]
export ADMIN_AWS_ACCESS_KEY_ID=[secret]
export ADMIN_AWS_SECRET_ACCESS_KEY=[secret]
export EXCLUDE_STREAM_CSV=[Optional CSV to exclude streams i.e. Exclude resource not by REST_RESOURCE_VERSION]
export INCLUDE_STREAM_CSV=[Optional CSV to include streams]
```

### New Session

```bash
export ENV=[environment]
export HOST=[host value]
export REST_RESOURCE_VERSION=[resource version]
export ADMIN_AWS_ACCESS_KEY_ID=[secret]
export ADMIN_AWS_SECRET_ACCESS_KEY=[secret]
export EXCLUDE_STREAM_CSV=[Optional CSV to exclude streams i.e. Exclude resource not in REST_RESOURCE_VERSION]
export INCLUDE_STREAM_CSV=[Optional CSV to include streams]
```

***Note: replace [variable description] with actual values***

### Create and Run Tests

Create tests within the `tap_rest_template/tests` subfolder and
  then run:

```bash
poetry run pycodestyle
poetry run coverage run -m pytest
poetry run coverage run -m pytest tap_rest_template/tests/test_med*
poetry run coverage html -d tap_rest_template/tests/codecoverage
```

***Note: Large test `test_lrg_00_core` requires a valid host***

You can also test the `tap-rest-template` CLI interface directly using `poetry run`:

```bash
poetry run tap-rest-template --help
poetry run tap-rest-template --version
poetry run tap-rest-template --about
```

## Testing with [Meltano](meltano.com) using target-jsonl

```bash
meltano invoke tap-rest-template --version
meltano elt tap-rest-template target-jsonl
```

***Target `target-jsonl` will move streams to the `output/` folder with a `.jsonl` suffix

### SDK Dev Guide

See the [dev guide](../../docs/dev_guide.md) for more instructions on how to use the Meltano SDK to
develop your own Singer taps and targets.
