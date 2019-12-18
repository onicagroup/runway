"""Environment variable lookup."""
from typing import Any, TYPE_CHECKING  # noqa

from .base import LookupHandler

if TYPE_CHECKING:
    from ...context import Context  # noqa: F401

TYPE_NAME = "env"


class EnvLookup(LookupHandler):
    """Environment variable lookup."""

    @classmethod
    def handle(cls, value, context, **_):
        # type: (str, 'Context', Any) -> Any
        """Retrieve an environment variable.

        The value is retrieved from a copy of the current environment variables
        that is saved to the context object. These environment variables
        are manipulated at runtime by Runway to fill in additional values
        such as ``DEPLOY_ENVIRONMENT`` and ``AWS_REGION`` to match the
        current execution.

        Args:
            value: The value passed to the lookup.
            context: The current context object.

        Raises:
            ValueError: Unable to find a value for the provided query and
                a default value was not provided.

        """
        query, args = cls.parse(value)

        result = context.env_vars.get(value, args.pop('default', None))

        if result:
            return cls.transform(result, to_type=args.pop('transform', None),
                                 **args)
        raise ValueError('"{}" does not exist in the environment'.format(value))
