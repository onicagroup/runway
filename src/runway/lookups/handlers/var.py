"""Variable definition lookup."""
# pylint: disable=arguments-differ
from typing import Any, TYPE_CHECKING  # pylint: disable=unused-import

import logging

from .base import LookupHandler

# python2 supported pylint sees this is cyclic even though its only for type checking
# pylint: disable=cyclic-import
if TYPE_CHECKING:
    from ...config import VariablesDefinition  # noqa: F401 pylint: disable=unused-import
    from ...context import Context  # noqa: F401 pylint: disable=unused-import


LOGGER = logging.getLogger('runway')
TYPE_NAME = 'var'


class VarLookup(LookupHandler):
    """Variable definition lookup."""

    @classmethod
    def handle(cls, value, variables, **_):
        # type: (str, 'Context', 'VariablesDefinition', Any) -> Any
        """Retrieve a variable from the variable definition.

        The value is retrieved from the variables passed to Runway using
        either a variables file or the ``variables`` directive of the
        config file.

        Args:
            value: The value passed to the lookup.
            variables: The resolved variables pass to Runway.

        Raises:
            ValueError: Unable to find a value for the provided query and
                a default value was not provided.

        """
        query, args = cls.parse(value)

        result = variables.find(query, default=args.pop('default', None))

        if result:
            return cls.transform(result, to_type=args.pop('transform', None),
                                 **args)

        raise ValueError('"{}" does not exist in the variable definition')
