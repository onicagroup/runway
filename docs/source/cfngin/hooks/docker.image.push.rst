#################
docker.image.push
#################

:Hook Path: ``runway.cfngin.hooks.docker.image.push``


Docker image push hook.

Replicates the functionality of the ``docker image push`` CLI command.


.. versionadded:: 1.18.0



****
Args
****

.. data:: ecr_repo
  :type: Optional[Dict[str, Optional[str]]]
  :value: None
  :noindex:

  Information describing an ECR repository. This is used to construct the repository URL.
  If providing a value for this field, do not provide a value for ``repo`` or ``image``.

  If using a private registry, only ``repo_name`` is required.
  If using a public registry, ``repo_name`` and ``registry_alias``.

  .. data:: account_id
    :type: Optional[str]
    :value: None
    :noindex:

    AWS account ID that owns the registry being logged into. If not provided,
    it will be acquired automatically if needed.

  .. data:: aws_region
    :type: Optional[str]
    :value: None
    :noindex:

    AWS region where the registry is located. If not provided, it will be acquired
    automatically if needed.

  .. data:: registry_alias
    :type: Optional[str]
    :value: None
    :noindex:

    If it is a public repository, provide the alias.

  .. data:: repo_name
    :type: str
    :noindex:

    The name of the repository.

.. data:: image
  :type: Optional[DockerImage]
  :value: None
  :noindex:

  A :class:`~runway.cfngin.hooks.docker.data_models.DockerImage` object.
  This can be retrieved from ``hook_data`` for a preceding :ref:`docker.image.build hook` using the
  :ref:`hook_data Lookup <hook_data lookup>`.

  If providing a value for this field, do not provide a value for ``ecr_repo`` or ``repo``.

.. data:: repo
  :type: Optional[str]
  :value: None
  :noindex:

  URI of a non Docker Hub repository where the image will be stored.
  If providing one of the other repo values or ``image``, leave this value empty.

.. data:: tags
  :type: Optional[List[str]]
  :value: ["latest"]
  :noindex:

  List of tags to push.



*******
Example
*******

.. code-block:: yaml

  pre_deploy:
    - path: runway.cfngin.hooks.docker.login
      args:
        ecr: true
        password: ${ecr login-password}
    - path: runway.cfngin.hooks.docker.image.build
      args:
        ecr_repo:
          repo_name: ${cfn ${namespace}-test-ecr.Repository}
        tags:
          - latest
          - python3.9
    - path: runway.cfngin.hooks.docker.image.push
      args:
        image: ${hook_data docker.image}

  stacks:
    ecr-lambda-function:
      class_path: blueprints.EcrFunction
      variables:
        ImageUri: ${hook_data docker.image.uri.latest}
