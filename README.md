# dhos-redis

A package that wraps redis functionality for Polaris.

## Maintainers
The Polaris platform was created by Sensyne Health Ltd., and has now been made open-source. As a result, some of the
instructions, setup and configuration will no longer be relevant to third party contributors. For example, some of
the libraries used may not be publicly available, or docker images may not be accessible externally. In addition, 
CICD pipelines may no longer function.

For now, Sensyne Health Ltd. and its employees are the maintainers of this repository.

## Setup
Assuming you are [set up](https://sensynehealth.atlassian.net/wiki/spaces/SENS/pages/3193270/Environment+setup):

`make install`

To run linters and test:

`make test`

## Usage
To use `dhos-redis` in your project, you'll need the following env vars:
- REDIS_HOST - the host for the redis connection (e.g. `localhost`)
- REDIS_PORT - the port number for the redis connection (e.g. `6379`)
- REDIS_PASSWORD - the password for the redis instance
- (Optional) REDIS_TIMEOUT - the timeout for the redis connection in seconds (defaults to `2`)

Then you can set and get at will (no initiation required):
```python
import dhosredis

dhosredis.set_value(key="KEY", value="VALUE")
print(dhosredis.get_value("KEY"))  # ==> "VALUE"
```

## Failed connection
Redis is designed to be used as a cache, rather than a source of truth.

**If dhosredis cannot connect to the specified redis instance, it will not raise an error.**

It will fail silently in the case of `set_value`, and will return the default value you specify (or `None`) in the case of `get_value`.

## Deploying
You can deploy via a merge to `main`. This will require a version bump in `setup.py`, and appropriate release notes in `RELEASES.md`.
