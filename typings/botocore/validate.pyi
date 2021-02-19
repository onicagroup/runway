"""
This type stub file was generated by pyright.
"""

"""User input parameter validation.

This module handles user input parameter validation
against a provided input model.

Note that the objects in this module do *not* mutate any
arguments.  No type version happens here.  It is up to another
layer to properly convert arguments to any required types.

Validation Errors
-----------------


"""

def validate_parameters(params, shape):
    """Validates input parameters against a schema.

    This is a convenience function that validates parameters against a schema.
    You can also instantiate and use the ParamValidator class directly if you
    want more control.

    If there are any validation errors then a ParamValidationError
    will be raised.  If there are no validation errors than no exception
    is raised and a value of None is returned.

    :param params: The user provided input parameters.

    :type shape: botocore.model.Shape
    :param shape: The schema which the input parameters should
        adhere to.

    :raise: ParamValidationError

    """
    ...

def type_check(valid_types): ...
def range_check(name, value, shape, error_type, errors): ...

class ValidationErrors(object):
    def __init__(self) -> None: ...
    def has_errors(self): ...
    def generate_report(self): ...
    def report(self, name, reason, **kwargs): ...

class ParamValidator(object):
    """Validates parameters against a shape model."""

    def validate(self, params, shape):
        """Validate parameters against a shape model.

        This method will validate the parameters against a provided shape model.
        All errors will be collected before returning to the caller.  This means
        that this method will not stop at the first error, it will return all
        possible errors.

        :param params: User provided dict of parameters
        :param shape: A shape model describing the expected input.

        :return: A list of errors.

        """
        ...
    _validate_float = ...

class ParamValidationDecorator(object):
    def __init__(self, param_validator, serializer) -> None: ...
    def serialize_to_request(self, parameters, operation_model): ...
