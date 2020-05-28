"""Pytest fixtures and plugins."""
# pylint: disable=redefined-outer-name
import logging
import os
from typing import Dict

import pytest
import yaml

from .factories import MockCFNginContext, MockRunwayConfig, MockRunwayContext

LOG = logging.getLogger(__name__)


@pytest.fixture(scope='session', autouse=True)
def aws_credentials():
    # type: () -> Dict[str, str]
    """Handle change in https://github.com/spulec/moto/issues/1924.

    Ensure AWS SDK finds some (bogus) credentials in the environment and
    doesn't try to use other providers.

    """
    overrides = {
        'AWS_ACCESS_KEY_ID': 'testing',
        'AWS_SECRET_ACCESS_KEY': 'testing',
        'AWS_DEFAULT_REGION': 'us-east-1'
    }
    saved_env = {}
    for key, value in overrides.items():
        LOG.info('Overriding env var: %s=%s', key, value)
        saved_env[key] = os.environ.get(key, None)
        os.environ[key] = value

    yield

    for key, value in saved_env.items():
        LOG.info('Restoring saved env var: %s=%s', key, value)
        if value is None:
            os.environ.pop(key, None)  # handle key missing
        else:
            os.environ[key] = value

    saved_env.clear()


@pytest.fixture(scope='package')
def fixture_dir():
    # type: () -> str
    """Path to the fixture directory."""
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'fixtures')
    return path


@pytest.fixture(scope='module')
def yaml_fixtures(request, fixture_dir):
    """Load test fixture yaml files.

    Uses a list of file paths within the fixture directory loaded from the
    `YAML_FIXTURES` variable of the module.

    """
    file_paths = getattr(request.module, 'YAML_FIXTURES', [])
    result = {}
    for file_path in file_paths:
        with open(os.path.join(fixture_dir, file_path)) as _file:
            data = _file.read()
            result[file_path] = yaml.safe_load(data)
    return result


@pytest.fixture(scope='function')
def cfngin_context(runway_context):
    """Create a mock CFNgin context object."""
    return MockCFNginContext(environment={},
                             boto3_credentials=runway_context.boto3_credentials,
                             region=runway_context.env_region)


@pytest.fixture
def patch_time(monkeypatch):
    """Patch built-in time object."""
    monkeypatch.setattr('time.sleep', lambda s: None)


@pytest.fixture(scope='function')
def patch_runway_config(request, monkeypatch, runway_config):
    """Patch Runway config and return a mock config object."""
    patch_path = getattr(request.module, 'PATCH_RUNWAY_CONFIG', None)
    if patch_path:
        monkeypatch.setattr(patch_path, runway_config)
    return runway_config


@pytest.fixture(scope='function')
def runway_config():
    """Create a mock runway config object."""
    return MockRunwayConfig()


@pytest.fixture(scope='function')
def runway_context(request):
    """Create a mock Runway context object."""
    env_vars = {
        'AWS_REGION': getattr(request.module, 'AWS_REGION', 'us-east-1'),
        'DEFAULT_AWS_REGION': getattr(request.module, 'AWS_REGION', 'us-east-1'),
        'DEPLOY_ENVIRONMET': getattr(request.module, 'DEPLOY_ENVIRONMET', 'test')
    }
    creds = {
        'AWS_ACCESS_KEY_ID': 'test_access_key',
        'AWS_SECRET_ACCESS_KEY': 'test_secret_key',
        'AWS_SESSION_TOKEN': 'test_session_token'
    }
    env_vars.update(getattr(request.module, 'AWS_CREDENTIALS', creds))
    env_vars.update(getattr(request.module, 'ENV_VARS', {}))
    return MockRunwayContext(env_name='test',
                             env_region='us-east-1',
                             env_root=os.getcwd(),
                             env_vars=env_vars,
                             command='test')
