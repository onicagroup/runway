#!/usr/bin/env bash

set -ev

if [ "$TRAVIS_OS_NAME" = "osx" ]; then
    # the only os that defaults 'python' to python2
    PYTHON="python3"
else
    PYTHON="python"
fi

if [ "$TRAVIS_OS_NAME" = "osx" ] || [ "$TRAVIS_OS_NAME" = "windows" ]; then
    # these do not nativly run in a venv
    PIPENV="pipenv run "
fi

${PIPENV}pytest

${PIPENV}flake8 --exclude=runway/cfngin,runway/embedded,runway/templates runway
find runway -name '*.py' -not -path 'runway/cfngin*' -not -path 'runway/embedded*' -not -path 'runway/templates/stacker/*' -not -path 'runway/templates/cdk-py/*' -not -path 'runway/blueprints/*' | xargs pipenv run ${PIPENV}pylint --rcfile=.pylintrc
find runway/blueprints -name '*.py' | xargs ${PIPENV}pylint --disable=duplicate-code
bash .travis/test_shim.sh
