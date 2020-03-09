"""Hook data lookup."""
# pylint: disable=arguments-differ,unused-argument
import logging
import warnings

from troposphere import BaseAWSObject
from runway.lookups.handlers.base import LookupHandler

LOGGER = logging.getLogger(__name__)
TYPE_NAME = "hook_data"


class HookDataLookup(LookupHandler):
    """Hook data lookup."""

    DEPRECATION_MSG = ('Lookup query syntax "<hook_name>::<key>" has been '
                       'deprecated. Please use the new lookup query syntax.')

    @classmethod
    def legacy_parse(cls, value):
        """Retain support for legacy lookup syntax.

        Args:
            value (str): Parameter(s) given to this lookup.

        Format of value:
            <hook_name>::<key>

        """
        hook_name, key = value.split("::")
        warnings.warn(cls.DEPRECATION_MSG, DeprecationWarning)
        LOGGER.warning(cls.DEPRECATION_MSG)
        return '{}.{}'.format(hook_name, key), {}

    @classmethod
    def handle(cls, value, context=None, provider=None, **kwargs):
        """Return the data from ``hook_data``.

        Args:
            value (str): Parameter(s) given to this lookup.
            context (:class:`runway.cfngin.context.Context`): Context instance.
            provider (:class:`runway.cfngin.providers.base.BaseProvider`):
                Provider instance.

        """
        try:
            query, args = cls.parse(value)
        except ValueError:
            query, args = cls.legacy_parse(value)

        result = context.hook_data.find(query, args.get('default'))

        if isinstance(result, BaseAWSObject) and \
                args.get('get') and \
                not args.get('load'):
            args['load'] = 'troposphere'

        if not result:
            raise ValueError('Could not find a value for "%s"' % value)

        if result == args.get('default'):
            # assume default value has already been processed so no need to
            # use these
            args.pop('load', None)
            args.pop('get', None)

        return cls.format_results(result, **args)
