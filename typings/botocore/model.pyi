"""
This type stub file was generated by pyright.
"""

from botocore.utils import CachedProperty, instance_cache

"""Abstractions to interact with service models."""
NOT_SET = object()
class NoShapeFoundError(Exception):
    ...


class InvalidShapeError(Exception):
    ...


class OperationNotFoundError(Exception):
    ...


class InvalidShapeReferenceError(Exception):
    ...


class ServiceId(str):
    def hyphenize(self):
        ...



class Shape(object):
    """Object representing a shape from the service model."""
    SERIALIZED_ATTRS = ...
    METADATA_ATTRS = ...
    MAP_TYPE = ...
    def __init__(self, shape_name, shape_model, shape_resolver=...) -> None:
        """

        :type shape_name: string
        :param shape_name: The name of the shape.

        :type shape_model: dict
        :param shape_model: The shape model.  This would be the value
            associated with the key in the "shapes" dict of the
            service model (i.e ``model['shapes'][shape_name]``)

        :type shape_resolver: botocore.model.ShapeResolver
        :param shape_resolver: A shape resolver object.  This is used to
            resolve references to other shapes.  For scalar shape types
            (string, integer, boolean, etc.), this argument is not
            required.  If a shape_resolver is not provided for a complex
            type, then a ``ValueError`` will be raised when an attempt
            to resolve a shape is made.

        """
        ...

    @CachedProperty
    def serialization(self):
        """Serialization information about the shape.

        This contains information that may be needed for input serialization
        or response parsing.  This can include:

            * name
            * queryName
            * flattened
            * location
            * payload
            * streaming
            * xmlNamespace
            * resultWrapper
            * xmlAttribute
            * jsonvalue
            * timestampFormat

        :rtype: dict
        :return: Serialization information about the shape.

        """
        ...

    @CachedProperty
    def metadata(self):
        """Metadata about the shape.

        This requires optional information about the shape, including:

            * min
            * max
            * enum
            * sensitive
            * required
            * idempotencyToken

        :rtype: dict
        :return: Metadata about the shape.

        """
        ...

    @CachedProperty
    def required_members(self):
        """A list of members that are required.

        A structure shape can define members that are required.
        This value will return a list of required members.  If there
        are no required members an empty list is returned.

        """
        ...

    def __repr__(self):
        ...

    @property
    def event_stream_name(self):
        ...



class StructureShape(Shape):
    @CachedProperty
    def members(self):
        ...

    @CachedProperty
    def event_stream_name(self):
        ...

    @CachedProperty
    def error_code(self):
        ...



class ListShape(Shape):
    @CachedProperty
    def member(self):
        ...



class MapShape(Shape):
    @CachedProperty
    def key(self):
        ...

    @CachedProperty
    def value(self):
        ...



class StringShape(Shape):
    @CachedProperty
    def enum(self):
        ...



class ServiceModel(object):
    """

    :ivar service_description: The parsed service description dictionary.

    """
    def __init__(self, service_description, service_name=...) -> None:
        """

        :type service_description: dict
        :param service_description: The service description model.  This value
            is obtained from a botocore.loader.Loader, or from directly loading
            the file yourself::

                service_description = json.load(
                    open('/path/to/service-description-model.json'))
                model = ServiceModel(service_description)

        :type service_name: str
        :param service_name: The name of the service.  Normally this is
            the endpoint prefix defined in the service_description.  However,
            you can override this value to provide a more convenient name.
            This is done in a few places in botocore (ses instead of email,
            emr instead of elasticmapreduce).  If this value is not provided,
            it will default to the endpointPrefix defined in the model.

        """
        ...

    def shape_for(self, shape_name, member_traits=...):
        ...

    def shape_for_error_code(self, error_code):
        ...

    def resolve_shape_ref(self, shape_ref):
        ...

    @CachedProperty
    def shape_names(self):
        ...

    @CachedProperty
    def error_shapes(self):
        ...

    @instance_cache
    def operation_model(self, operation_name):
        ...

    @CachedProperty
    def documentation(self):
        ...

    @CachedProperty
    def operation_names(self):
        ...

    @CachedProperty
    def service_name(self):
        """The name of the service.

        This defaults to the endpointPrefix defined in the service model.
        However, this value can be overriden when a ``ServiceModel`` is
        created.  If a service_name was not provided when the ``ServiceModel``
        was created and if there is no endpointPrefix defined in the
        service model, then an ``UndefinedModelAttributeError`` exception
        will be raised.

        """
        ...

    @CachedProperty
    def service_id(self):
        ...

    @CachedProperty
    def signing_name(self):
        """The name to use when computing signatures.

        If the model does not define a signing name, this
        value will be the endpoint prefix defined in the model.
        """
        ...

    @CachedProperty
    def api_version(self):
        ...

    @CachedProperty
    def protocol(self):
        ...

    @CachedProperty
    def endpoint_prefix(self):
        ...

    @CachedProperty
    def endpoint_discovery_operation(self):
        ...

    @CachedProperty
    def endpoint_discovery_required(self):
        ...

    @property
    def signature_version(self):
        ...

    @signature_version.setter
    def signature_version(self, value):
        ...

    def __repr__(self):
        ...



class OperationModel(object):
    def __init__(self, operation_model, service_model, name=...) -> None:
        """

        :type operation_model: dict
        :param operation_model: The operation model.  This comes from the
            service model, and is the value associated with the operation
            name in the service model (i.e ``model['operations'][op_name]``).

        :type service_model: botocore.model.ServiceModel
        :param service_model: The service model associated with the operation.

        :type name: string
        :param name: The operation name.  This is the operation name exposed to
            the users of this model.  This can potentially be different from
            the "wire_name", which is the operation name that *must* by
            provided over the wire.  For example, given::

               "CreateCloudFrontOriginAccessIdentity":{
                 "name":"CreateCloudFrontOriginAccessIdentity2014_11_06",
                  ...
              }

           The ``name`` would be ``CreateCloudFrontOriginAccessIdentity``,
           but the ``self.wire_name`` would be
           ``CreateCloudFrontOriginAccessIdentity2014_11_06``, which is the
           value we must send in the corresponding HTTP request.

        """
        ...

    @CachedProperty
    def name(self):
        ...

    @property
    def wire_name(self):
        """The wire name of the operation.

        In many situations this is the same value as the
        ``name``, value, but in some services, the operation name
        exposed to the user is different from the operaiton name
        we send across the wire (e.g cloudfront).

        Any serialization code should use ``wire_name``.

        """
        ...

    @property
    def service_model(self):
        ...

    @CachedProperty
    def documentation(self):
        ...

    @CachedProperty
    def deprecated(self):
        ...

    @CachedProperty
    def endpoint_discovery(self):
        ...

    @CachedProperty
    def is_endpoint_discovery_operation(self):
        ...

    @CachedProperty
    def input_shape(self):
        ...

    @CachedProperty
    def output_shape(self):
        ...

    @CachedProperty
    def idempotent_members(self):
        ...

    @CachedProperty
    def auth_type(self):
        ...

    @CachedProperty
    def error_shapes(self):
        ...

    @CachedProperty
    def endpoint(self):
        ...

    @CachedProperty
    def http_checksum_required(self):
        ...

    @CachedProperty
    def has_event_stream_input(self):
        ...

    @CachedProperty
    def has_event_stream_output(self):
        ...

    def get_event_stream_input(self):
        ...

    def get_event_stream_output(self):
        ...

    @CachedProperty
    def has_streaming_input(self):
        ...

    @CachedProperty
    def has_streaming_output(self):
        ...

    def get_streaming_input(self):
        ...

    def get_streaming_output(self):
        ...

    def __repr__(self):
        ...



class ShapeResolver(object):
    """Resolves shape references."""
    SHAPE_CLASSES = ...
    def __init__(self, shape_map) -> None:
        ...

    def get_shape_by_name(self, shape_name, member_traits=...):
        ...

    def resolve_shape_ref(self, shape_ref):
        ...



class UnresolvableShapeMap(object):
    """A ShapeResolver that will throw ValueErrors when shapes are resolved.
    """
    def get_shape_by_name(self, shape_name, member_traits=...):
        ...

    def resolve_shape_ref(self, shape_ref):
        ...



class DenormalizedStructureBuilder(object):
    """Build a StructureShape from a denormalized model.

    This is a convenience builder class that makes it easy to construct
    ``StructureShape``s based on a denormalized model.

    It will handle the details of creating unique shape names and creating
    the appropriate shape map needed by the ``StructureShape`` class.

    Example usage::

        builder = DenormalizedStructureBuilder()
        shape = builder.with_members({
            'A': {
                'type': 'structure',
                'members': {
                    'B': {
                        'type': 'structure',
                        'members': {
                            'C': {
                                'type': 'string',
                            }
                        }
                    }
                }
            }
        }).build_model()
        # ``shape`` is now an instance of botocore.model.StructureShape

    :type dict_type: class
    :param dict_type: The dictionary type to use, allowing you to opt-in
                      to using OrderedDict or another dict type. This can
                      be particularly useful for testing when order
                      matters, such as for documentation.

    """
    def __init__(self, name=...) -> None:
        ...

    def with_members(self, members):
        """

        :type members: dict
        :param members: The denormalized members.

        :return: self

        """
        ...

    def build_model(self):
        """Build the model based on the provided members.

        :rtype: botocore.model.StructureShape
        :return: The built StructureShape object.

        """
        ...



class ShapeNameGenerator(object):
    """Generate unique shape names for a type.

    This class can be used in conjunction with the DenormalizedStructureBuilder
    to generate unique shape names for a given type.

    """
    def __init__(self) -> None:
        ...

    def new_shape_name(self, type_name):
        """Generate a unique shape name.

        This method will guarantee a unique shape name each time it is
        called with the same type.

        ::

            >>> s = ShapeNameGenerator()
            >>> s.new_shape_name('structure')
            'StructureType1'
            >>> s.new_shape_name('structure')
            'StructureType2'
            >>> s.new_shape_name('list')
            'ListType1'
            >>> s.new_shape_name('list')
            'ListType2'


        :type type_name: string
        :param type_name: The type name (structure, list, map, string, etc.)

        :rtype: string
        :return: A unique shape name for the given type

        """
        ...
