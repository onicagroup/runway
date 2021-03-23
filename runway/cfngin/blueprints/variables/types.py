"""CFNgin blueprint variable types."""
# pylint: disable=invalid-name,len-as-condition
from __future__ import annotations

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, overload

from troposphere import BaseAWSObject

_TroposphereType = TypeVar("_TroposphereType", bound=BaseAWSObject)


class TroposphereType(Generic[_TroposphereType]):
    """Represents a Troposphere type.

    :class:`Troposphere` will convert the value provided to the variable to
    the specified Troposphere type.

    Both resource and parameter classes (which are just used to configure
    other resources) are acceptable as configuration values.

    Complete resource definitions must be dictionaries, with the keys
    identifying the resource titles, and the values being used as the
    constructor parameters.

    Parameter classes can be defined as dictionary or a list of
    dictionaries. In either case, the keys and values will be used directly
    as constructor parameters.

    """

    def __init__(
        self,
        defined_type: Type[_TroposphereType],
        many: bool = False,
        optional: bool = False,
        validate: bool = True,
    ) -> None:
        """Instantiate class.

        Args:
            defined_type: Troposphere type.
            many: Whether or not multiple resources can be constructed.
                If the defined type is a resource, multiple resources can be
                passed as a dictionary of dictionaries.
                If it is a parameter class, multiple resources are passed as
                a list.
            optional: Whether an undefined/null configured value is acceptable.
                In that case a value of ``None`` will be passed to the template,
                even if ``many`` is enabled.
            validate: Whether to validate the generated object on creation.
                Should be left enabled unless the object will be augmented with
                mandatory parameters in the template code, such that it must be
                validated at a later point.

        """
        self._validate_type(defined_type)

        self._type = defined_type
        self._many = many
        self._optional = optional
        self._validate = validate

    @staticmethod
    def _validate_type(defined_type: Type[_TroposphereType]) -> None:
        if not hasattr(defined_type, "from_dict"):
            raise ValueError("Type must have `from_dict` attribute")

    @property
    def resource_name(self) -> str:
        """Name of the type or resource."""
        return str(getattr(self._type, "resource_name", None) or self._type.__name__)

    @overload
    def create(self, value: Dict[str, Any]) -> _TroposphereType:
        ...

    @overload
    def create(self, value: List[Dict[str, Any]]) -> List[_TroposphereType]:
        ...

    @overload
    def create(self, value: None) -> None:
        ...

    def create(
        self, value: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]
    ) -> Optional[Union[_TroposphereType, List[_TroposphereType]]]:
        """Create the troposphere type from the value.

        Args:
            value: A dictionary or list of dictionaries (see class documentation
                for details) to use as parameters to create the Troposphere type instance.
                Each dictionary will be passed to the ``from_dict`` method of
                the type.

        Returns:
            Returns the value converted to the troposphere type.

        """
        # Explicitly check with len such that non-sequence types throw.
        if self._optional and (value is None or len(value) == 0):
            return None

        if hasattr(self._type, "resource_type"):
            # Our type is a resource, so ensure we have a dict of title to
            # parameters
            if not isinstance(value, dict):
                raise ValueError(
                    "Resources must be specified as a dict of title to parameters"
                )
            if not self._many and len(value) > 1:
                raise ValueError(
                    "Only one resource can be provided for this "
                    "TroposphereType variable"
                )

            result = [self._type.from_dict(title, v) for title, v in value.items()]
        else:
            # Our type is for properties, not a resource, so don't use
            # titles
            if self._many and isinstance(value, list):
                result = [self._type.from_dict(None, v) for v in value]
            elif not isinstance(value, dict):
                raise ValueError(
                    "TroposphereType for a single non-resource"
                    "type must be specified as a dict of "
                    "parameters"
                )
            else:
                result = [self._type.from_dict(None, value)]

        if self._validate:
            for v in result:
                v._validate_props()

        # TODO: figure out why pyright does not like this
        return result[0] if not self._many else result  # type: ignore


class CFNType:
    """Represents a CloudFormation Parameter Type.

    :class:`CFNType` can be used as the ``type`` for a Blueprint variable.
    Unlike other variables, a variable with ``type: CFNType``, will
    be submitted to CloudFormation as a Parameter.

    """

    def __init__(self, parameter_type: str) -> None:
        """Instantiate class.

        Args:
            parameter_type: An AWS specific parameter type. (http://goo.gl/PthovJ)

        """
        self.parameter_type = parameter_type


# General CFN types
CFNString = CFNType("String")
CFNNumber = CFNType("Number")
CFNNumberList = CFNType("List<Number>")
CFNCommaDelimitedList = CFNType("CommaDelimitedList")

# AWS-Specific Parameter Types
# https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html#aws-specific-parameter-types
EC2AvailabilityZoneName = CFNType("AWS::EC2::AvailabilityZone::Name")
EC2ImageId = CFNType("AWS::EC2::Image::Id")
EC2InstanceId = CFNType("AWS::EC2::Instance::Id")
EC2KeyPairKeyName = CFNType("AWS::EC2::KeyPair::KeyName")
EC2SecurityGroupGroupName = CFNType("AWS::EC2::SecurityGroup::GroupName")
EC2SecurityGroupId = CFNType("AWS::EC2::SecurityGroup::Id")
EC2SubnetId = CFNType("AWS::EC2::Subnet::Id")
EC2VolumeId = CFNType("AWS::EC2::Volume::Id")
EC2VPCId = CFNType("AWS::EC2::VPC::Id")
Route53HostedZoneId = CFNType("AWS::Route53::HostedZone::Id")
EC2AvailabilityZoneNameList = CFNType("List<AWS::EC2::AvailabilityZone::Name>")
EC2ImageIdList = CFNType("List<AWS::EC2::Image::Id>")
EC2InstanceIdList = CFNType("List<AWS::EC2::Instance::Id>")
EC2SecurityGroupGroupNameList = CFNType("List<AWS::EC2::SecurityGroup::GroupName>")
EC2SecurityGroupIdList = CFNType("List<AWS::EC2::SecurityGroup::Id>")
EC2SubnetIdList = CFNType("List<AWS::EC2::Subnet::Id>")
EC2VolumeIdList = CFNType("List<AWS::EC2::Volume::Id>")
EC2VPCIdList = CFNType("List<AWS::EC2::VPC::Id>")
Route53HostedZoneIdList = CFNType("List<AWS::Route53::HostedZone::Id>")

# SSM Parameter Types
# https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html#aws-ssm-parameter-types
SSMParameterName = CFNType("AWS::SSM::Parameter::Name")
SSMParameterValueString = CFNType("AWS::SSM::Parameter::Value<String>")
SSMParameterValueStringList = CFNType("AWS::SSM::Parameter::Value<List<String>>")
SSMParameterValueCommaDelimitedList = CFNType(
    "AWS::SSM::Parameter::Value<CommaDelimitedList>"
)
# Each AWS-specific type here is repeated from the the list above
SSMParameterValueEC2AvailabilityZoneName = CFNType(
    "AWS::SSM::Parameter::Value<AWS::EC2::AvailabilityZone::Name>"
)
SSMParameterValueEC2ImageId = CFNType("AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>")
SSMParameterValueEC2InstanceId = CFNType(
    "AWS::SSM::Parameter::Value<AWS::EC2::Instance::Id>"
)
SSMParameterValueEC2KeyPairKeyName = CFNType(
    "AWS::SSM::Parameter::Value<AWS::EC2::KeyPair::KeyName>"
)
SSMParameterValueEC2SecurityGroupGroupName = CFNType(
    "AWS::SSM::Parameter::Value<AWS::EC2::SecurityGroup::GroupName>"
)
SSMParameterValueEC2SecurityGroupId = CFNType(
    "AWS::SSM::Parameter::Value<AWS::EC2::SecurityGroup::Id>"
)
SSMParameterValueEC2SubnetId = CFNType(
    "AWS::SSM::Parameter::Value<AWS::EC2::Subnet::Id>"
)
SSMParameterValueEC2VolumeId = CFNType(
    "AWS::SSM::Parameter::Value<AWS::EC2::Volume::Id>"
)
SSMParameterValueEC2VPCId = CFNType("AWS::SSM::Parameter::Value<AWS::EC2::VPC::Id>")
SSMParameterValueRoute53HostedZoneId = CFNType(
    "AWS::SSM::Parameter::Value<AWS::Route53::HostedZone::Id>"
)
SSMParameterValueEC2AvailabilityZoneNameList = CFNType(
    "AWS::SSM::Parameter::Value<List<AWS::EC2::AvailabilityZone::Name>>"
)
SSMParameterValueEC2ImageIdList = CFNType(
    "AWS::SSM::Parameter::Value<List<AWS::EC2::Image::Id>>"
)
SSMParameterValueEC2InstanceIdList = CFNType(
    "AWS::SSM::Parameter::Value<List<AWS::EC2::Instance::Id>>"
)
SSMParameterValueEC2SecurityGroupGroupNameList = CFNType(
    "AWS::SSM::Parameter::Value<List<AWS::EC2::SecurityGroup::GroupName>>"
)
SSMParameterValueEC2SecurityGroupIdList = CFNType(
    "AWS::SSM::Parameter::Value<List<AWS::EC2::SecurityGroup::Id>>"
)
SSMParameterValueEC2SubnetIdList = CFNType(
    "AWS::SSM::Parameter::Value<List<AWS::EC2::Subnet::Id>>"
)
SSMParameterValueEC2VolumeIdList = CFNType(
    "AWS::SSM::Parameter::Value<List<AWS::EC2::Volume::Id>>"
)
SSMParameterValueEC2VPCIdList = CFNType(
    "AWS::SSM::Parameter::Value<List<AWS::EC2::VPC::Id>>"
)
SSMParameterValueRoute53HostedZoneIdList = CFNType(
    "AWS::SSM::Parameter::Value<List<AWS::Route53::HostedZone::Id>>"
)
