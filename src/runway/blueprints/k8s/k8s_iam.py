#!/usr/bin/env python
"""Module with k8s IAM resources."""
from __future__ import print_function

from troposphere import AccountId, Join, Output, iam

import awacs.autoscaling
import awacs.sts
from awacs.aws import Allow, PolicyDocument, Principal, Statement
from awacs.helpers.trust import make_simple_assume_policy

from stacker.blueprints.base import Blueprint
from stacker.blueprints.variables.types import CFNString

IAM_POLICY_ARN_PREFIX = 'arn:aws:iam::aws:policy/'


class Iam(Blueprint):
    """Stacker blueprint for creating k8s IAM resources."""

    VARIABLES = {
        'EksClusterName': {'type': CFNString,
                           'description': 'Name of the Kubernetes cluster',
                           'min_length': 2,
                           'max_length': 40}
    }

    def create_template(self):
        """Create template (main function called by Stacker)."""
        template = self.template
        variables = self.get_variables()
        template.add_version('2010-09-09')
        template.add_description('Kubernetes IAM policies - V1.0.0')

        # Resources
        nodeinstancerole = template.add_resource(
            iam.Role(
                'NodeInstanceRole',
                AssumeRolePolicyDocument=make_simple_assume_policy(
                    'ec2.amazonaws.com'
                ),
                ManagedPolicyArns=[
                    IAM_POLICY_ARN_PREFIX + i for i in [
                        'AmazonEKSWorkerNodePolicy',
                        'AmazonEKS_CNI_Policy',
                        'AmazonEC2ContainerRegistryReadOnly',
                        # SSM agent not shipped ootb
                        # 'AmazonSSMManagedInstanceCore'
                    ]
                ]
            )
        )
        template.add_output(
            Output(
                'NodeInstanceRole',
                Description='The node instance role name',
                Value=nodeinstancerole.ref()
            )
        )
        template.add_output(
            Output(
                'NodeInstanceRoleArn',
                Description='The node instance role ARN',
                Value=nodeinstancerole.get_att('Arn')
            )
        )

        nodeinstanceprofile = template.add_resource(
            iam.InstanceProfile(
                'NodeInstanceProfile',
                Path='/',
                Roles=[nodeinstancerole.ref()]
            )
        )
        template.add_output(
            Output(
                'NodeInstanceProfile',
                Description='The node instance profile',
                Value=nodeinstanceprofile.ref()
            )
        )
        template.add_output(
            Output(
                'NodeInstanceProfileArn',
                Description='The node instance profile ARN',
                Value=nodeinstanceprofile.get_att('Arn')
            )
        )

        kiaminstancerole = template.add_resource(
            iam.Role(
                'KiamInstanceRole',
                AssumeRolePolicyDocument=make_simple_assume_policy(
                    'ec2.amazonaws.com'
                ),
                ManagedPolicyArns=[
                    IAM_POLICY_ARN_PREFIX + i for i in [
                        'AmazonEKSWorkerNodePolicy',
                        'AmazonEKS_CNI_Policy',
                        'AmazonEC2ContainerRegistryReadOnly'
                    ]
                ],
                Policies=[
                    iam.Policy(
                        PolicyName='sts-assumerole',
                        PolicyDocument=PolicyDocument(
                            Version='2012-10-17',
                            Statement=[
                                Statement(
                                    Action=[awacs.sts.AssumeRole],
                                    Effect=Allow,
                                    Resource=[
                                        Join('',
                                             ['arn:aws:iam::',
                                              AccountId,
                                              ':role/',
                                              variables['EksClusterName'].ref,
                                              '-pod-role-*'])
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )
        )
        template.add_output(
            Output(
                'KiamInstanceRole',
                Description='The kiam instance role name',
                Value=kiaminstancerole.ref()
            )
        )
        template.add_output(
            Output(
                'KiamInstanceRoleArn',
                Description='The kiam instance role ARN',
                Value=kiaminstancerole.get_att('Arn')
            )
        )

        kiaminstanceprofile = template.add_resource(
            iam.InstanceProfile(
                'KiamInstanceProfile',
                Path='/',
                Roles=[kiaminstancerole.ref()]
            )
        )
        template.add_output(
            Output(
                'KiamInstanceProfile',
                Description='The kiam instance profile',
                Value=kiaminstanceprofile.ref()
            )
        )
        template.add_output(
            Output(
                'KiamInstanceProfileArn',
                Description='The kiam instance profile ARN',
                Value=kiaminstanceprofile.get_att('Arn')
            )
        )

        template.add_resource(
            iam.Role(
                'ClusterAutoScalerInstanceRole',
                AssumeRolePolicyDocument=PolicyDocument(
                    Version='2012-10-17',
                    Statement=[
                        Statement(
                            Effect=Allow,
                            Action=[awacs.sts.AssumeRole],
                            Principal=Principal('Service',
                                                'ec2.amazonaws.com')
                        ),
                        Statement(
                            Effect=Allow,
                            Action=[awacs.sts.AssumeRole],
                            Principal=Principal(
                                'AWS',
                                kiaminstancerole.get_att('Arn')
                            )
                        )
                    ]
                ),
                Policies=[
                    iam.Policy(
                        PolicyName='cluster-autoscaler',
                        PolicyDocument=PolicyDocument(
                            Version='2012-10-17',
                            Statement=[
                                Statement(
                                    Action=[awacs.autoscaling.DescribeAutoScalingGroups,  # noqa
                                            awacs.autoscaling.DescribeAutoScalingInstances,  # noqa
                                            awacs.autoscaling.DescribeTags,
                                            awacs.autoscaling.SetDesiredCapacity,  # noqa
                                            awacs.autoscaling.TerminateInstanceInAutoScalingGroup],  # noqa pylint: disable=line-too-long
                                    Effect=Allow,
                                    Resource=['*']
                                )
                            ]
                        )
                    )
                ]
            )
        )


# Helper section to enable easy blueprint -> template generation
# (just run `python <thisfile>` to output the json)
if __name__ == "__main__":
    from stacker.context import Context
    print(Iam('test', Context({"namespace": "test"}), None).to_json())
