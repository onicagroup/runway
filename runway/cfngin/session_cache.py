"""CFNgin session caching."""
import logging
from typing import Optional

import boto3

from runway.aws_sso_botocore.session import Session

from .ui import ui

LOGGER = logging.getLogger(__name__)

DEFAULT_PROFILE = None
# A global credential cache that can be shared among boto3 sessions. This is
# inherently threadsafe thanks to the GIL:
# https://docs.python.org/3/glossary.html#term-global-interpreter-lock
CREDENTIAL_CACHE = {}


def get_session(
    region: Optional[str] = None,
    profile: Optional[str] = None,
    access_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    session_token=None,
) -> boto3.Session:
    """Create a thread-safe boto3 session.

    Args:
        region: The region for the session.
        profile: The profile for the session.
        access_key: AWS Access Key ID.
        secret_key: AWS secret Access Key.
        session_token: AWS session token.

    Returns:
        A thread-safe boto3 session.

    """
    if profile:
        LOGGER.debug(
            'building session using profile "%s" in region "%s"',
            profile,
            region or "default",
        )
    elif access_key:
        LOGGER.debug(
            'building session with Access Key "%s" in region "%s"',
            access_key,
            region or "default",
        )

    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        aws_session_token=session_token,
        botocore_session=Session(),  # type: ignore
        region_name=region,
        profile_name=profile,
    )
    cred_provider = session._session.get_component("credential_provider")  # type: ignore
    provider = cred_provider.get_provider("assume-role")
    provider.cache = CREDENTIAL_CACHE
    provider._prompter = ui.getpass
    return session
