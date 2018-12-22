.. _repo-structure:

Repo Structure
==============

Projects deployed via runway can be structured in a few ways; some examples
follow:

Git Branches as Environments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This example shows 2 modules using environment git branches (these same files
would be present in each environment branch, with changes to any environment
promoted through branches)::

    .
    ├── myapp.cfn
    │   ├── dev-us-west-2.env
    │   ├── prod-us-west-2.env
    │   ├── myapp.yaml
    │   └── templates
    │       └── foo.json
    ├── myapp.tf
    │   ├── backend.tfvars
    │   ├── dev-us-east-1.tfvars
    │   ├── prod-us-east-1.tfvars
    │   └── main.tf
    └── runway.yml

Directories as Environments
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Another sample repo structure, showing the same modules nested in environment folders::

    .
    ├── dev
    │   ├── myapp.cfn
    │   │   ├── dev-us-west-2.env
    │   │   ├── myapp.yaml
    │   │   └── templates
    │   │       └── myapp_cf_template.json
    │   ├── myapp.tf
    │   │   ├── backend.tfvars
    │   │   ├── dev-us-east-1.tfvars
    │   │   └── main.tf
    │   └── runway.yml
    └── prod
        ├── myapp.cfn
        │   ├── prod-us-west-2.env
        │   ├── myapp.yaml
        │   └── templates
        │       └── myapp_cf_template.json
        ├── myapp.tf
        │   ├── backend.tfvars
        │   ├── prod-us-east-1.tfvars
        │   └── main.tf
        └── runway.yml

Directories as Environments with a Single Module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Another sample repo structure, showing environment folders containing a single 
CloudFormation module at their root (combining the `current_dir` & `ignore_git_branch` 
"Runway Config File" options to merge the Environment & Module folders)::

    .
    ├── dev
    │   ├── dev-us-west-2.env
    │   ├── myapp.yaml
    │   ├── runway.yml
    │   └── templates
    │       └── myapp_cf_template.json
    └── prod
        ├── prod-us-west-2.env
        ├── myapp.yaml
        ├── runway.yml
        └── templates
            └── myapp_cf_template.json
