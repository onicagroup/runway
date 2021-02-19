"""Runway exceptions."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, List, Optional

if TYPE_CHECKING:
    from .variables import (
        Variable,
        VariableValue,
        VariableValueConcatenation,
        VariableValueLookup,
    )


class ConfigNotFound(Exception):
    """Configuration file could not be found."""

    looking_for: List[str]
    message: str
    path: Path

    def __init__(self, *, looking_for: Optional[List[str]] = None, path: Path) -> None:
        """Instantiate class.

        Args:
            path: Path where the config file was expected to be found.
            looking_for: List of file names that were being looked for.

        """
        self.looking_for = looking_for or []
        self.path = path

        if looking_for:
            self.message = (
                f"config file not found at path {path}; "
                f"looking for one of {looking_for}"
            )
        else:
            self.message = f"config file not found at path {path}"
        super().__init__(self.message, self.path, self.looking_for)


class FailedLookup(Exception):
    """Intermediary Exception to be converted to FailedVariableLookup.

    Should be caught by error handling and
    :class:`runway.cfngin.exceptions.FailedVariableLookup` raised instead to
    construct a propper error message.

    """

    lookup: VariableValueLookup
    cause: Exception

    def __init__(
        self, lookup: VariableValueLookup, cause: Exception, *args: Any, **kwargs: Any
    ) -> None:
        """Instantiate class.

        Args:
            lookup: The variable value lookup that was attempted and
                resulted in an exception being raised.
            cause: The exception that was raised.

        """
        self.lookup = lookup
        self.cause = cause
        super().__init__("Failed lookup", *args, **kwargs)


class FailedVariableLookup(Exception):
    """Lookup could not be resolved.

    Raised when an exception is raised when trying to resolve a lookup.

    """

    cause: FailedLookup
    variable: Variable

    def __init__(
        self, variable: Variable, lookup_error: FailedLookup, *args: Any, **kwargs: Any
    ) -> None:
        """Instantiate class.

        Args:
            variable: The variable containing the failed lookup.
            lookup_error: The exception that was raised directly before this one.

        """
        self.variable = variable
        self.cause = lookup_error
        super().__init__(
            f'Could not resolve lookup "{lookup_error.lookup}" for variable "{variable.name}"',
            *args,
            **kwargs
        )


class InvalidLookupConcatenation(Exception):
    """Invalid return value for a concatinated (chained) lookup.

    The return value must be a string when lookups are concatinated.

    """

    concatenated_lookups: VariableValueConcatenation[Any]
    invalid_lookup: VariableValue

    def __init__(
        self,
        invalid_lookup: VariableValue,
        concat_lookups: VariableValueConcatenation[Any],
        *args: Any,
        **kwargs: Any
    ) -> None:
        """Instantiate class."""
        self.concatenated_lookups = concat_lookups
        self.invalid_lookup = invalid_lookup
        message = (
            f"expected return value of type {str} but received "
            f'{type(invalid_lookup.value)} for lookup "{invalid_lookup}" '
            f'in "{concat_lookups}"'
        )
        super().__init__(message, *args, **kwargs)


class NpmNotFound(Exception):
    """Raised when npm could not be executed or was not found in path."""

    message: str

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Instantiate class."""
        self.message = (
            '"npm" not found in path or is not executable; '
            "please ensure it is installed correctly"
        )
        super().__init__(self.message, *args, **kwargs)


class OutputDoesNotExist(Exception):
    """Raised when a specific stack output does not exist."""

    def __init__(self, stack_name: str, output: str, *args: Any, **kwargs: Any) -> None:
        """Instantiate class.

        Args:
            stack_name: Name of the stack.
            output: The output that does not exist.

        """
        self.stack_name = stack_name
        self.output = output

        message = "Output %s does not exist on stack %s" % (output, stack_name)
        super().__init__(message, *args, **kwargs)


class UnknownLookupType(Exception):
    """Lookup type provided does not match a registered lookup.

    Example:
        If a lookup of ``${<lookup_type> query}`` is used and ``<lookup_type>``
        is not a registered lookup, this exception will be raised.

    """

    def __init__(self, lookup: VariableValueLookup, *args: Any, **kwargs: Any) -> None:
        """Instantiate class.

        Args:
            lookup: Variable value lookup that could not find a handler.

        """
        message = f'Unknown lookup type "{lookup.lookup_name.value}" in "{lookup}"'
        super().__init__(message, *args, **kwargs)


class UnresolvedVariable(Exception):
    """Raised when trying to use a variable before it has been resolved."""

    def __init__(self, variable: Variable, *args: Any, **kwargs: Any) -> None:
        """Instantiate class.

        Args:
            variable: The unresolved variable.

        """
        message = 'Attempted to use variable "{}" before it was resolved'.format(
            variable.name
        )
        super().__init__(message, *args, **kwargs)


class UnresolvedVariableValue(Exception):
    """Intermediary Exception to be converted to UnresolvedVariable.

    Should be caught by error handling and
    :class:`runway.cfngin.exceptions.UnresolvedVariable` raised instead to
    construct a propper error message.

    """

    lookup: VariableValueLookup

    def __init__(self, lookup: VariableValueLookup, *args: Any, **kwargs: Any) -> None:
        """Instantiate class.

        Args:
            lookup: The variable value lookup that is not resolved.

        """
        self.lookup = lookup
        super().__init__("Unresolved lookup", *args, **kwargs)


class VariablesFileNotFound(Exception):
    """Defined variables file could not be found."""

    file_path: Path
    message: str

    def __init__(self, file_path: Path) -> None:
        """Instantiate class.

        Args:
            file_path: Path where the file was expected to be found.

        """
        self.file_path = file_path
        self.message = f"defined variables file not found at path {file_path}"
        super().__init__(self.file_path, self.message)
