.. _runway-config-options:

Runway Config File
==================

runway.yml sample::

    ---
    # Order that modules will be deployed. A module will be skipped if a
    # corresponding env/config file is not present in its folder.
    # (e.g., for cfn modules, if a dev-us-west-2.env file is not in the 'app.cfn'
    # folder when running a dev deployment of 'app' to us-west-2 then it will be
    # skipped.)
    deployments:
      - name: app1
        modules:
          - myapp.cfn
        regions:
          - us-west-2

      - name: app2
        modules:
          - myapp.tf
        regions:
          - us-east-1
        assume-role:  # optional
          # When running multiple deployments, post_deploy_env_revert can be used
          # to revert the AWS credentials in the environment to their previous
          # values
          # post_deploy_env_revert: true
          dev: arn:aws:iam::account-id1:role/role-name
          prod: arn:aws:iam::account-id2:role/role-name
          # A single ARN can be specified instead, to apply to all environments
          # arn: arn:aws:iam::account-id:role/role-name
          # Role duration can be set at the top level, or in a specific environment
          # duration: 7200
          # dev:
          #   arn: arn:aws:iam::account-id1:role/role-name
          #   duration: 7200
        account-alias:  # optional
          # A mapping of environment -> alias mappings can be provided to have
          # Runway verify the current assumed role / credentials match the
          # necessary account
          dev: my_dev_account
          prod: my_dev_account
        account-id:  # optional
          # A mapping of environment -> id mappings can be provided to have Runway
          # verify the current assumed role / credentials match the necessary
          # account
          dev: 123456789012
          prod: 345678901234
        env_vars:  # optional environment variable overrides
          dev:
            AWS_PROFILE: foo
            APP_PATH:  # When specified as list, will be treated as components of a path on disk
              - myapp.tf
              - foo
          prod:
            AWS_PROFILE: bar
            APP_PATH:
              - myapp.tf
              - foo
          "*":  # Applied to all environments
            ANOTHER_VAR: foo
        skip-npm-ci: false  # optional, and should rarely be used. Omits npm ci
                            # execution during Serverless deployments
                            # (i.e. for use with pre-packaged node_modules)
    
    # If using environment folders instead of git branches, git branch lookup can
    # be disabled entirely (see "Repo Structure")
    # ignore_git_branch: true

runway.yml can also be placed in a module folder (e.g. a repo/environment containing 
only one module doesn't need to nest the module in a subfolder)::

    ---
    # This will deploy the module in which runway.yml is located
    deployments:
      - current_dir: true
        regions:
          - us-west-2
        assume-role:
          arn: arn:aws:iam::account-id:role/role-name
    
    # If using environment folders instead of git branches, git branch lookup can
    # be disabled entirely (see "Repo Structure"). See "Directories as Environments
    # with a Single Module" in "Repo Structure".
    # ignore_git_branch: true
