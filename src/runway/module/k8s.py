"""K8s (kustomize) module."""

import logging
import os
import subprocess
import sys

import six

from runway.module import RunwayModule, run_module_command
from runway.kbenv import KBEnvManager
from runway.util import which

LOGGER = logging.getLogger('runway')


def gen_overlay_dirs(environment, region):
    """Generate possible overlay directories."""
    return [
        # Give preference to explicit environment-region dirs
        "%s-%s" % (environment, region),
        # Fallback to environment name only
        environment
    ]


def get_module_defined_k8s_ver(k8s_version_opts, env_name):
    """Return version of Terraform requested in module options."""
    if isinstance(k8s_version_opts, six.string_types):
        return k8s_version_opts
    if k8s_version_opts.get(env_name):
        return k8s_version_opts.get(env_name)
    if k8s_version_opts.get('*'):
        return k8s_version_opts.get('*')
    return None


def get_overlay_dir(overlays_path, environment, region):
    """Determine overlay directory to use."""
    for name in gen_overlay_dirs(environment, region):
        overlay_dir = os.path.join(overlays_path, name)
        if os.path.isfile(os.path.join(overlay_dir, 'kustomization.yaml')):
            return overlay_dir
    return overlay_dir  # fallback to last dir


def generate_response(overlay_path, module_path, environment, region):
    """Determine if environment is defined."""
    configfile = os.path.join(overlay_path, 'kustomization.yaml')
    if os.path.isdir(overlay_path) and os.path.isfile(configfile):
        LOGGER.info("Processing kustomize overlay: %s", configfile)
        return {'skipped_configs': False}
    LOGGER.error("No kustomize overlay for this environment/region found -- "
                 "looking for one of \"%s\"",
                 ', '.join(
                     [os.path.join(module_path, 'overlays', i, 'kustomization.yaml')  # noqa
                      for i in gen_overlay_dirs(environment, region)]
                 ))
    return {'skipped_configs': True}


class K8s(RunwayModule):
    """Kubectl Runway Module."""

    def run_kubectl(self, command='plan'):
        """Run kubectl."""
        kustomize_config_path = os.path.join(
            self.path,
            'overlays',
            get_overlay_dir(os.path.join(self.path,
                                         'overlays'),
                            self.context.env_name,
                            self.context.env_region)
        )
        response = generate_response(kustomize_config_path,
                                     self.path,
                                     self.context.env_name,
                                     self.context.env_region)
        if response['skipped_configs']:
            return response

        module_defined_k8s_ver = get_module_defined_k8s_ver(
            self.options.get('options', {}).get('kubectl_version', {}),
            self.context.env_name
        )
        if module_defined_k8s_ver:
            k8s_bin = KBEnvManager(self.path).install(module_defined_k8s_ver)
        elif os.path.isfile(os.path.join(kustomize_config_path,
                                         '.kubectl-version')):
            k8s_bin = KBEnvManager(kustomize_config_path).install()
        elif os.path.isfile(os.path.join(self.path,
                                         '.kubectl-version')):
            k8s_bin = KBEnvManager(self.path).install()
        elif os.path.isfile(os.path.join(self.context.env_root,
                                         '.kubectl-version')):
            k8s_bin = KBEnvManager(self.context.env_root).install()
        else:
            if not which('kubectl'):
                LOGGER.error('kubectl not available (a '
                             '".kubectl-version" file is not present '
                             'and "kubectl" not found in path). Fix '
                             'this by writing a desired kubectl version '
                             'to your module\'s .kubectl-version file '
                             'or installing kubectl.')
                sys.exit(1)
            k8s_bin = 'kubectl'

        kustomize_cmd = [k8s_bin, 'kustomize', kustomize_config_path]
        kustomize_yml = subprocess.check_output(kustomize_cmd,
                                                env=self.context.env_vars)
        if command == 'plan':
            LOGGER.info('The following yaml was generated by '
                        'kubectl:\n\n%s', kustomize_yml)
        else:
            LOGGER.debug('The following yaml was generated by '
                         'kubectl:\n\n%s', kustomize_yml)
        if command in ['apply', 'delete']:
            kubectl_command = [k8s_bin, command, '-k', kustomize_config_path]
            LOGGER.info('Running kubectl %s ("%s")...',
                        command,
                        ' '.join(kubectl_command))
            run_module_command(kubectl_command, self.context.env_vars)
        return response

    def plan(self):
        """Run kustomize build and display generated plan."""
        self.run_kubectl(command='plan')

    def deploy(self):
        """Run kubectl apply."""
        self.run_kubectl(command='apply')

    def destroy(self):
        """Run kubectl delete."""
        self.run_kubectl(command='delete')
