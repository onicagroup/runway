.. _CFNgin: ../cfngin/index.html
.. _Lookups: lookups.html

.. _mod-cfn:

CloudFormation
==============

CloudFormation modules are managed by 2 files:

- a key/value environment file
- a yaml file defining the stacks/templates/params.

.. rubric:: Environment

Name these files in the form of ``ENV-REGION.env`` (e.g. ``dev-us-east-1.env``) or ``ENV.env`` (e.g. ``dev.env``)::

    # Namespace is used as each stack's prefix
    # We recommend an (org/customer)/environment delineation
    namespace: contoso-dev
    environment: dev
    customer: contoso
    region: us-west-2
    # The stacker bucket is the S3 bucket (automatically created) where templates
    # are uploaded for deployment (a CloudFormation requirement for large templates)
    stacker_bucket_name: stacker-contoso-us-west-2

.. rubric:: Stack Config (yaml file)

These files can have any name ending in .yaml (they will be evaluated in alphabetical order)::

    # Note namespace/stacker_bucket_name being substituted from the environment
    namespace: ${namespace}
    stacker_bucket: ${stacker_bucket_name}

    stacks:
      myvpcstack:  # will be deployed as contoso-dev-myvpcstack
        template_path: templates/vpc.yaml
        # The enabled option is optional and defaults to true. You can use it to
        # enable/disable stacks per-environment (i.e. like the namespace
        # substitution above, but with the value of either true or false for the
        # enabled option here)
        enabled: true
      myvpcendpoint:
        template_path: templates/vpcendpoint.yaml
        # variables map directly to CFN parameters; here used to supply the
        # VpcId output from the myvpcstack to the VpcId parameter of this stack
        variables:
          VpcId: ${output myvpcstack::VpcId}

The config yaml supports many more features; see the full CFNgin_ documentation for more detail
(e.g. stack configuration options, additional lookups in addition to output (e.g. SSM, DynamoDB))


Environment Values Via Runway Deployment/Module Options
---------------------------------------------------------

In addition or in place of the environment file(s), deploy environment specific
values can be provided via deployment and module options as ``parameters``. It
is recommended to use `Lookups`_ in the ``parameters`` section to
assist in selecting the appropriate values for the deploy environment and/or
region being deployed to but, this is not a requirement if the value will
remain the same.


Top-level Runway Config
~~~~~~~~~~~~~~~~~~~~~~~

::

    ---

    deployments:
      - modules:
          - path: mycfnstacks
            parameters:
              namespace: contoso-${env DEPLOY_ENVIRONMENT}
              foo: bar
              some_value: ${var some_map.${env DEPLOY_ENVIRONMENT}}

and/or

::

    ---

    deployments:
      - parameters:
          namespace: contoso-${env DEPLOY_ENVIRONMENT}
          foo: bar
          some_value: ${var some_map.${env DEPLOY_ENVIRONMENT}}
        modules:
          - mycfnstacks


In Module Directory
~~~~~~~~~~~~~~~~~~~

.. important: `Lookups`_ are not supported in this file.

::

    ---
    parameters:
      namespace: contoso-dev
      foo: bar

(in ``runway.module.yml``)
