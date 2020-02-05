Lookups
=======

.. _Lookups:

Runway Lookups allow the use of variables within the Runway config file. These
variables can then be passed along to :ref:`deployments <runway-deployment>`,
:ref:`modules <runway-module>` and :ref:`tests <runway-test>`.

The syntax for a lookup is ``${<lookup-name> <query>::<arg-key>=<arg-value>}``

+---------------------------+-------------------------------------------------+
| Component                 | Description                                     |
+===========================+=================================================+
| ``${``                    | Signifies the opening of the lookup.            |
+---------------------------+-------------------------------------------------+
| ``<lookup-name>``         | The name of the lookup you wish to use. (e.g.   |
|                           | ``env``)                                        |
+---------------------------+-------------------------------------------------+
| `` ``                     | The separator between lookup name a query.      |
+---------------------------+-------------------------------------------------+
| ``<query>``               | The value the lookup will be looking for. (e.g. |
|                           | ``AWS_REGION``)                                 |
|                           | | When using a lookup on a dictionary/mapping,  |
|                           | like  for the `var`_ lookup, you can get nested |
|                           | values by providing the full path to the value. |
|                           | (e.g. ``ami.dev``}                              |
+---------------------------+-------------------------------------------------+
| ``::``                    | The separator between a query and optional      |
|                           | arguments.                                      |
+---------------------------+-------------------------------------------------+
| ``<arg-key>=<arg-value>`` | An argument passed to a lookup. Multiple        |
|                           | arguments can be passed to a lookup by          |
|                           | separating them with a comma (``,``). Arguments |
|                           | are optional. Supported arguments depend on the |
|                           | lookup being used.                              |
+---------------------------+-------------------------------------------------+

Lookups can be nested (e.g. ``${var ami_id.${var AWS_REGION}}``).

Lookups can't resolve other lookups. For example, if i use ``${var region}`` in
my Runway config file to resolve the ``region`` from my variables file, the
value in the variables file can't be ``${env AWS_REGION}``. Well, it can but
it will resolve to the literal value provided, not an AWS region like you may
expect.

.. automodule:: runway.lookups.handlers.base

Build-in Lookups
^^^^^^^^^^^^^^^^

.. _build-in-lookups:

env
~~~

.. _env-lookup:

.. automodule:: runway.lookups.handlers.env

var
~~~

.. _var-lookup:

.. automodule:: runway.lookups.handlers.var
