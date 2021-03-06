"""Packaging settings."""
from codecs import open as codecs_open
from os.path import abspath, dirname, join

from setuptools import find_packages, setup

THIS_DIR = abspath(dirname(__file__))


def local_scheme(version: str) -> str:  # pylint: disable=unused-argument
    """Skip the local version (eg. +xyz) to upload to Test PyPI."""
    return ""


with codecs_open(join(THIS_DIR, "README.md"), encoding="utf-8") as readfile:
    LONG_DESCRIPTION = readfile.read()


INSTALL_REQUIRES = [
    "Send2Trash",
    "awacs",  # for embedded hooks
    'backports.cached_property ; python_version < "3.8"',
    "botocore>=1.19.36<2.0",
    "boto3>=1.16.36<2.0",
    "cfn_flip>=1.2.1",  # 1.2.1+ require PyYAML 4.1+
    "cfn-lint",
    "click>=7.1",
    "coloredlogs",
    "docker",
    "requests",
    "pydantic>=1.4.0",
    "pyhcl~=0.4",  # does not support HCL2, possibly move to extras_require in the future
    "python-hcl2~=2.0",
    "typing_extensions",  # only really needed for < 3.8 but can still be used in >= 3.8
    "gitpython",
    'importlib-metadata; python_version < "3.8"',
    "packaging",  # component of setuptools needed for version compare
    "pyOpenSSL",  # For embedded hook & associated script usage
    "PyYAML>=5",
    "yamllint",
    "zgitignore",  # for embedded hooks
    "troposphere>=2.4.2",
    # botocore pins its urllib3 dependency like this, so we need to do the
    "urllib3>=1.25.4,<1.27",
    "jinja2>=2.7,<3.0",
    "formic2",
]


setup(
    name="runway",
    description="Simplify infrastructure/app testing/deployment",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/onicagroup/runway",
    author="Onica Group LLC",
    author_email="opensource@onica.com",
    license="Apache License 2.0",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.7",
    keywords="cli",
    packages=find_packages(exclude=("integration*", "tests*")),
    install_requires=INSTALL_REQUIRES,
    setup_requires=["setuptools_scm"],
    use_scm_version={"local_scheme": local_scheme},
    entry_points={"console_scripts": ["runway=runway._cli.main:cli"]},
    scripts=[
        "scripts/tf-runway",
        "scripts/tf-runway.cmd",
        "scripts/tfenv-runway",
        "scripts/tfenv-runway.cmd",
    ],
    include_package_data=True,  # needed for templates,blueprints,hooks
)
