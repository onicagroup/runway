"""Base class for CFNgin hooks."""
# pylint: disable=unused-argument
from collections import UserDict
import logging
from typing import Any

from troposphere import Tags
from runway.util import MutableMap

from ..actions import build
from ..context import Context
from ..plan import COLOR_CODES
from ..providers.aws.default import Provider
from ..stack import Stack
from ..status import COMPLETE, FAILED, PENDING, SUBMITTED

LOGGER = logging.getLogger(__name__)


class Hook(object):
    """Base class for hooks.

    Not all hooks need to be classes and not all classes need to be hooks.

    Attributes:
        args (MutableMap): Keyword arguments passed to the hook, loaded into
            a MutableMap object.
        blueprint (Optional[Blueprint]): Blueprint generated by the hook if
            it will be deploying a stack.
        context (Context): Context instance. (passed in by CFNgin)
        provider (BaseProvider): Provider instance. (passed in by CFNgin)
        stack (Optional[Stack]): Stack object if the hook deploys a stack.
        stack_name (str): Name of the stack created by the hook if a stack is
            to be created.

    """

    def __init__(self,
                 context: Context,
                 provider: Provider,
                 **kwargs: Any
                 ) -> None:
        """Instantiate class.

        Args:
            context (:class:`runway.cfngin.context.Context`): Context instance.
                (passed in by CFNgin)
            provider (:class:`runway.cfngin.providers.base.BaseProvider`):
                Provider instance. (passed in by CFNgin)

        """
        kwargs.setdefault('tags', {})

        self.args = MutableMap(**kwargs)
        self.args.tags.update(context.tags)
        self.blueprint = None
        self.context = context
        self.provider = provider
        self.stack = None
        self.stack_name = 'stack'
        self._deploy_action = HookBuildAction(self.context, self.provider)

    @property
    def tags(self):
        """Return tags that should be applied to any resource being created.

        Returns:
            troposphere.Tags

        """
        return Tags(**dict(self.context.tags, **self.args.tags.data))

    def generate_stack(self, **kwargs):
        """Create a CFNgin Stack object.

        Returns:
            Stack

        """
        definition = HookStackDefinition(name=self.stack_name,
                                         tags=self.args.tags.data,
                                         **kwargs)
        stack = Stack(definition, self.context)
        stack._blueprint = self.blueprint  # pylint: disable=protected-access
        return stack

    def get_template_description(self, suffix=None):
        """Generate a template description.

        Args:
            suffix (Optional[str]): Suffix to append to the end of a
                CloudFormation template description.

        Returns:
            str: CloudFormation template description.

        """
        template = 'Automatically generated by {}'
        if suffix:
            template += ' - {}'
            return template.format(self.__class__.__module__, suffix)
        return template.format(self.__class__.__module__)

    def deploy_stack(self, stack=None, wait=False):
        """Deploy a stack.

        Args:
            stack (Optional[Stack]): A stack to deploy.
            wait (bool): Wither to wait for the stack to complete before
                returning.

        Returns:
            Status: Ending status of the stack.

        """
        stack = stack or self.stack
        status = self._deploy_action.run(stack=stack, status=PENDING)
        self._log_stack(stack, status)

        if wait:
            status = self.wait_for_stack(stack=stack, status=status)
        return status

    def post_deploy(self):
        """Run during the **post_deploy** stage."""
        raise NotImplementedError

    def post_destroy(self):
        """Run during the **post_destroy** stage."""
        raise NotImplementedError

    def pre_deploy(self):
        """Run during the **pre_deploy** stage."""
        raise NotImplementedError

    def pre_destroy(self):
        """Run during the **pre_destroy** stage."""
        raise NotImplementedError

    def wait_for_stack(self, stack=None, status=None):
        """Wait for a CloudFormation stack to complete.

        Args:
            stack (Optional[Stack]): A stack that has been acted upon.
            status (Optional[Status]): The last status of the stack.

        Returns:
            Status: Ending status of the stack.

        """
        status = status or SUBMITTED
        stack = stack or self.stack

        while True:
            if status in (COMPLETE, FAILED):
                break
            LOGGER.warning('Waiting for stack to complete...')
            status = self._deploy_action.run(stack=stack, status=status)

        self._log_stack(stack, status)
        return status

    @staticmethod
    def _log_stack(stack, status):
        """Log stack status. Mimics normal stack deployment.

        Args:
            stack (:class:`runway.cfngin.stack.Stack`): The stack being logged.
            status (:class:`runway.cfngin.status.Status`) The status being
                logged.

        """
        msg = "%s: %s" % (stack.name, status.name)
        if status.reason:
            msg += " (%s)" % (status.reason)
        color_code = COLOR_CODES.get(status.code, 37)
        LOGGER.info(msg, extra={"color": color_code})


class HookBuildAction(build.Action):
    """Build action that can be used from hooks."""

    def __init__(self, context, provider):
        """Instantiate class.

        Args:
            context (:class:`runway.cfngin.context.Context`): The context
                for the current run.

        """
        super(HookBuildAction, self).__init__(context)
        self._provider = provider

    @property
    def provider(self):
        """Override the inherited property to return the local provider."""
        return self._provider

    def build_provider(self, stack):
        """Override the inherited method to always return local provider."""
        return self._provider

    def run(self, **kwargs):
        """Run the action for one stack."""
        return self._launch_stack(**kwargs)


class HookStackDefinition(UserDict):
    """Stack definition for use in hooks to avoid cyclic imports."""

    def __init__(self, name, **kwargs):
        """Instantiate class."""
        values = {
            'class_path': None,
            'enabled': True,
            'in_progress_behavior': None,
            'name': name,
            'locked': False,
            'profile': None,
            'protected': False,
            'region': None,
            'required_by': None,
            'requires': None,
            'stack_name': None,
            'stack_policy_path': None,
            'tags': None,
            'template_path': None,
            'variables': None
        }
        values.update(kwargs)
        super(HookStackDefinition, self).__init__(**values)

    def __getattr__(self, key):
        """Implement dot notation."""
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)
