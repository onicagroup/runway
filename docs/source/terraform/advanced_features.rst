.. _Runway Config File: runway_config.html

#################
Advanced Features
#################

Advanced features and detailed information for using Terraform with Runway.


.. contents::
  :depth: 4


.. _tf-backend:

*********************
Backend Configuration
*********************

If your Terraform will only ever be used with a single backend, it can be defined inline.

.. rubric:: main.tf
.. code-block::

  terraform {
    backend "s3" {
      region = "us-east-1"
      key = "some_unique_identifier_for_my_module"
      bucket = "some_s3_bucket_name"
      dynamodb_table = "some_ddb_table_name"
    }
  }

However, it's generally preferable to separate the backend configuration out from the rest of the Terraform code.
This form of configuration is known as `partial configuration`_ and allows for dynamic or secret values to be passed in at runtime.

Below are examples of how to implement `partial configuration`_ with Runway.
All examples provided showcase the use of the s3 backend type as it is the easiest to use when going from zero to deployed (try :ref:`runway gen-sample cfngin <command-gen-sample>` for quickstart Terraform backend infrastructure).
However, Runway supports the use of any `backend type <https://www.terraform.io/docs/backends/types/index.html>`__ (refer to Terraform's documentation for proper `partial configuration`_ instructions).

.. seealso::
  https://www.terraform.io/docs/backends/config.html#partial-configuration
    Terraform partial configuration

  https://www.terraform.io/docs/backends/types/index.html
    Terraform backend types

.. _partial configuration: https://www.terraform.io/docs/backends/config.html#partial-configuration


Backend Config File
===================

Backend config options can be specified in a separate file or multiple files per environment and/or region using one of the following naming schemes.

- *backend-ENV-REGION.(hcl|tfvars)*
- *backend-ENV.(hcl|tfvars)*
- *backend-REGION.(hcl|tfvars)*
- *backend.(hcl|tfvars)*

.. rubric:: Example
.. code-block::

  region = "us-east-1"
  bucket = "some_s3_bucket_name"
  dynamodb_table = "some_ddb_table_name"

In the above example, where all but the key are defined, the **main.tf** backend definition is reduced to the following.

.. rubric:: main.tf
.. code-block::

  terraform {
    backend "s3" {
      key = "some_unique_identifier_for_my_module"
    }
  }

.. versionchanged:: 1.11.0
  Added support for hcl files.


runway.yml
==========

Backend config options can also be specified as a module option in the `Runway Config File`_.
:ref:`Lookups` can be used to provide dynamic values to this option.

.. important::
  There has been a *bug* since Terraform 0.12 that prevents passing blocks to ``-backend-config`` (`issue <https://github.com/hashicorp/terraform/issues/21830>`__).
  This means that for backends that use blocks in their config (e.g. remote), the blocks must be provided via file.
  Attributes are unaffected.

  .. code-block::
    :caption: backend.hcl

    workspaces {
      prefix = "example-"
    }

.. code-block:: yaml
  :caption: Module Level

  deployments:
    - modules:
        - path: sampleapp-01.tf
          options:
            terraform_backend_config:
              bucket: mybucket
              dynamodb_table: mytable
              region: us-east-1
        - path: sampleapp-02.tf
          options:
            terraform_backend_config:
              bucket: ${cfn common-tf-state.TerraformStateBucketName}
              dynamodb_table: ${cfn common-tf-state.TerraformStateTableName}
              region: ${env AWS_REGION}

.. code-block:: yaml
  :caption: Deployment Level

  deployments:
    - modules:
        - path: sampleapp-01.tf
        - path: sampleapp-02.tf
      module_options:  # shared between all modules in deployment
        terraform_backend_config:
          bucket: ${ssm ParamNameHere::region=us-east-1}
          dynamodb_table: ${ssm ParamNameHere::region=us-east-1}
          region: ${env AWS_REGION}


----


.. _tf-args:

******************************************
Specifying Terraform CLI Arguments/Options
******************************************

Runway can pass custom arguments/options to the Terraform CLI by using the ``args`` option.

The value of ``args`` can be provided in one of two ways.
The simplest way is to provide a *list* of arguments/options which will be appended to ``terraform apply`` when executed by Runway.
Each element of the argument/option should be it's own list item (e.g. ``-parallelism=25 -no-color`` would be ``['-parallelism=25, '-no-color']``).

For more control, a map can be provided to pass arguments/options to other commands.
Arguments can be passed to ``terraform apply``, ``terraform init``, and/or ``terraform plan`` by using the *action* as the key in the map (see the **Runway Example** section below).
The value of each key in the map must be a list as described in the previous section.

.. important::
  The following arguments/options are provided by Runway and should not be provided manually:
  *auto-approve*, *backend-config*, *force*, *no-color*, *reconfigure*, *update*, and *var-file*.
  Providing any of these manually could result in unintended side-effects.

.. code-block:: yaml
  :caption: Runway Example

  deployments:
    - modules:
        - path: sampleapp-01.tf
          options:
            args:
              - '-no-color'
              - '-parallelism=25'
        - path: sampleapp-02.tf
          options:
            args:
              apply:
                - '-no-color'
                - '-parallelism=25'
              init:
                - '-no-color'
              plan:
                - '-no-color'
                - '-parallelism=25'
      regions:
        - us-east-2
      environments:
        example: true

.. code-block:: sh
  :caption: Command Equivalent

  # runway deploy - sampleapp-01.tf
  terraform init -reconfigure
  terraform apply -no-color -parallelism=25 -auto-approve=false

  # runway plan - sampleapp-01.tf
  terraform plan

  # runway deploy - sampleapp-02.tf
  terraform init -reconfigure -no-color
  terraform apply -no-color -parallelism=25 -auto-approve=false

  # runway plan - sampleapp-02.tf
  terraform plan -no-color -parallelism=25


----


.. _tf-version:

******************
Version Management
******************

By specifying which version of Terraform to use via a ``.terraform-version`` file in your module directory or in :attr:`deployment.module_options`/:attr:`module.options`, Runway will automatically download & use that version for the module.
This, alongside tightly pinning Terraform provider versions, is highly recommended to keep a predictable experience when deploying your module.

.. code-block:: text
  :caption: .terraform-version

  0.11.6

.. code-block:: yaml
  :caption: runway.yml

  deployments:
    - modules:
        - path: sampleapp-01.tf
          options:
            terraform_version: 0.11.13

Without a version specified, Runway will fallback to whatever ``terraform`` it finds first in your PATH.
