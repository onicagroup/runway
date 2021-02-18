"""
This type stub file was generated by pyright.
"""

import logging
from collections import namedtuple

logger = logging.getLogger(__name__)
_NodeList = namedtuple('NodeList', ['first', 'middle', 'last'])
_FIRST = 0
_MIDDLE = 1
_LAST = 2
class NodeList(_NodeList):
    def __copy__(self):
        ...



def first_non_none_response(responses, default=...):
    """Find first non None response in a list of tuples.

    This function can be used to find the first non None response from
    handlers connected to an event.  This is useful if you are interested
    in the returned responses from event handlers. Example usage::

        print(first_non_none_response([(func1, None), (func2, 'foo'),
                                       (func3, 'bar')]))
        # This will print 'foo'

    :type responses: list of tuples
    :param responses: The responses from the ``EventHooks.emit`` method.
        This is a list of tuples, and each tuple is
        (handler, handler_response).

    :param default: If no non-None responses are found, then this default
        value will be returned.

    :return: The first non-None response in the list of tuples.

    """
    ...

class BaseEventHooks(object):
    def emit(self, event_name, **kwargs):
        """Call all handlers subscribed to an event.

        :type event_name: str
        :param event_name: The name of the event to emit.

        :type **kwargs: dict
        :param **kwargs: Arbitrary kwargs to pass through to the
            subscribed handlers.  The ``event_name`` will be injected
            into the kwargs so it's not necesary to add this to **kwargs.

        :rtype: list of tuples
        :return: A list of ``(handler_func, handler_func_return_value)``

        """
        ...

    def register(self, event_name, handler, unique_id=..., unique_id_uses_count=...):
        """Register an event handler for a given event.

        If a ``unique_id`` is given, the handler will not be registered
        if a handler with the ``unique_id`` has already been registered.

        Handlers are called in the order they have been registered.
        Note handlers can also be registered with ``register_first()``
        and ``register_last()``.  All handlers registered with
        ``register_first()`` are called before handlers registered
        with ``register()`` which are called before handlers registered
        with ``register_last()``.

        """
        ...

    def register_first(self, event_name, handler, unique_id=..., unique_id_uses_count=...):
        """Register an event handler to be called first for an event.

        All event handlers registered with ``register_first()`` will
        be called before handlers registered with ``register()`` and
        ``register_last()``.

        """
        ...

    def register_last(self, event_name, handler, unique_id=..., unique_id_uses_count=...):
        """Register an event handler to be called last for an event.

        All event handlers registered with ``register_last()`` will be called
        after handlers registered with ``register_first()`` and ``register()``.

        """
        ...

    def unregister(self, event_name, handler=..., unique_id=..., unique_id_uses_count=...):
        """Unregister an event handler for a given event.

        If no ``unique_id`` was given during registration, then the
        first instance of the event handler is removed (if the event
        handler has been registered multiple times).

        """
        ...



class HierarchicalEmitter(BaseEventHooks):
    def __init__(self) -> None:
        ...

    def emit(self, event_name, **kwargs):
        """
        Emit an event by name with arguments passed as keyword args.

            >>> responses = emitter.emit(
            ...     'my-event.service.operation', arg1='one', arg2='two')

        :rtype: list
        :return: List of (handler, response) tuples from all processed
                 handlers.
        """
        ...

    def emit_until_response(self, event_name, **kwargs):
        """
        Emit an event by name with arguments passed as keyword args,
        until the first non-``None`` response is received. This
        method prevents subsequent handlers from being invoked.

            >>> handler, response = emitter.emit_until_response(
                'my-event.service.operation', arg1='one', arg2='two')

        :rtype: tuple
        :return: The first (handler, response) tuple where the response
                 is not ``None``, otherwise (``None``, ``None``).
        """
        ...

    def unregister(self, event_name, handler=..., unique_id=..., unique_id_uses_count=...):
        ...

    def __copy__(self):
        ...



class EventAliaser(BaseEventHooks):
    def __init__(self, event_emitter, event_aliases=...) -> None:
        ...

    def emit(self, event_name, **kwargs):
        ...

    def emit_until_response(self, event_name, **kwargs):
        ...

    def register(self, event_name, handler, unique_id=..., unique_id_uses_count=...):
        ...

    def register_first(self, event_name, handler, unique_id=..., unique_id_uses_count=...):
        ...

    def register_last(self, event_name, handler, unique_id=..., unique_id_uses_count=...):
        ...

    def unregister(self, event_name, handler=..., unique_id=..., unique_id_uses_count=...):
        ...

    def __copy__(self):
        ...



class _PrefixTrie(object):
    """Specialized prefix trie that handles wildcards.

    The prefixes in this case are based on dot separated
    names so 'foo.bar.baz' is::

        foo -> bar -> baz

    Wildcard support just means that having a key such as 'foo.bar.*.baz' will
    be matched with a call to ``get_items(key='foo.bar.ANYTHING.baz')``.

    You can think of this prefix trie as the equivalent as defaultdict(list),
    except that it can do prefix searches:

        foo.bar.baz -> A
        foo.bar -> B
        foo -> C

    Calling ``get_items('foo.bar.baz')`` will return [A + B + C], from
    most specific to least specific.

    """
    def __init__(self) -> None:
        ...

    def append_item(self, key, value, section=...):
        """Add an item to a key.

        If a value is already associated with that key, the new
        value is appended to the list for the key.
        """
        ...

    def prefix_search(self, key):
        """Collect all items that are prefixes of key.

        Prefix in this case are delineated by '.' characters so
        'foo.bar.baz' is a 3 chunk sequence of 3 "prefixes" (
        "foo", "bar", and "baz").

        """
        ...

    def remove_item(self, key, value):
        """Remove an item associated with a key.

        If the value is not associated with the key a ``ValueError``
        will be raised.  If the key does not exist in the trie, a
        ``ValueError`` will be raised.

        """
        ...

    def __copy__(self):
        ...
