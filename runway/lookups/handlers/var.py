"""Retrieve a variable from the variables file or definition.

If the Lookup is unable to find an defined variable matching the
provided query, the default value is returned or a ``ValueError`` is raised
if a default value was not provided.

Nested values can be used by providing the full path to the value but, it
will not select a list element.

The returned value can contain any YAML support data type
(dictionaries/mappings/hashes, lists/arrays/sequences, strings, numbers,
and booleon).


.. rubric:: Arguments

This Lookup supports all :ref:`Common Lookup Arguments` but, the folling have
limited or no effect:

- region


.. rubric:: Example
.. code-block:: yaml

  deployment:
    - modules:
        - path: sampleapp.cfn
          parameters:
            ami_id: ${var ami_id.${env AWS_REGION}}
      env_vars:
        SOME_VARIABLE: ${var some_variable::default=default}

"""
# pyright: reportIncompatibleMethodOverride=none
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from .base import LookupHandler

if TYPE_CHECKING:
    from ...util import MutableMap


LOGGER = logging.getLogger(__name__)
TYPE_NAME = "var"


class VarLookup(LookupHandler):
    """Variable definition Lookup."""

    @classmethod
    def handle(  # pylint: disable=arguments-differ
        cls, value: str, *__args: Any, variables: MutableMap, **__kwargs: Any
    ) -> Any:
        """Retrieve a variable from the variable definition.

        The value is retrieved from the variables passed to Runway using
        either a variables file or the ``variables`` directive of the
        config file.

        Args:
            value: The value passed to the Lookup.
            variables: The resolved variables pass to Runway.

        Raises:
            ValueError: Unable to find a value for the provided query and
                a default value was not provided.

        """
        query, args = cls.parse(value)

        result = variables.find(query, default=args.pop("default", ""))

        if result != "":  # allows for False bool and NoneType results
            return cls.format_results(result, **args)

        raise ValueError('"{}" does not exist in the variable definition'.format(query))
