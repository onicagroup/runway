"""Test runway.core.components._module."""
# pylint: disable=no-self-use,protected-access
import logging
import sys

import pytest
import six
import yaml
from mock import MagicMock, call, patch

from runway.core.components import Deployment, Module
from runway.config import FutureDefinition

MODULE = 'runway.core.components._module'


class TestModule(object):
    """Test runway.core.components._module.Module."""

    def test_init(self):
        """Test init."""
        mock_ctx = MagicMock()
        mock_def = MagicMock()
        mock_def.name = 'module-name'
        mock_vars = MagicMock()

        mod = Module(context=mock_ctx,
                     definition=mock_def,
                     variables=mock_vars)

        mock_ctx.copy.assert_called_once_with()
        assert mod.ctx == mock_ctx.copy()
        mock_def.resolve.assert_called_once_with(mock_ctx.copy(), mock_vars)
        assert mod.name == 'module-name'

    def test_child_modules(self, fx_deployments, runway_context):
        """Test child_modules."""
        deployment = Deployment(context=runway_context,
                                definition=fx_deployments.load('simple_parallel_module'))
        mod0 = Module(context=runway_context,
                      definition=deployment.definition.modules[0],
                      deployment=deployment.definition)
        mod1 = Module(context=runway_context,
                      definition=deployment.definition.modules[1],
                      deployment=deployment.definition)

        assert len(mod0.child_modules) == 2
        assert not mod1.child_modules

        for index, child in enumerate(mod0.child_modules):
            assert isinstance(child, Module)
            # basic checks to ensure the child was setup correctly
            assert child.ctx.env.name == runway_context.env.name
            assert child.definition == mod0.definition.child_modules[index]

    @patch(MODULE + '.ModulePath')
    def test_path(self, mock_path, fx_deployments, runway_context):
        """Test path."""
        mock_path.return_value = 'module-path'
        mod = Module(context=runway_context,
                     definition=fx_deployments.load('min_required').modules[0])

        assert mod.path == 'module-path'
        mock_path.assert_called_once_with(mod.definition,
                                          runway_context.env.root_dir,
                                          str(runway_context.env.root_dir /
                                              '.runway_cache'))

    def test_payload(self, cd_tmp_path, fx_deployments, runway_context):
        """Test payload."""
        runway_context.env.root_dir = cd_tmp_path
        mod_dir = cd_tmp_path / 'sampleapp-01.cfn'
        mod_dir.mkdir()
        opts = {
            'env_vars': {'dev': {'map-var': 'incorrect'},
                         'test': {'map-var': 'map-val'}},
            'environments': {'test': ['us-east-1']},
            'options': {'local-opt': 'local-opt-val'},
            'parameters': {'local-param': 'local-param-val'}
        }
        (mod_dir / 'runway.module.yml').write_text(six.u(yaml.safe_dump(opts)))
        mod = Module(context=runway_context,
                     definition=fx_deployments.load('simple_env_vars_map').modules[0])
        result = mod.payload
        # assert not result

        assert mod.ctx.env.vars['deployment_var'] == 'val'
        assert mod.ctx.env.vars['map-var'] == opts['env_vars']['test']['map-var']
        assert result['environments'] == opts['environments']
        assert result['environment'] == opts['environments']['test']
        assert result['options'] == opts['options']
        assert result['parameters'] == opts['parameters']

    @pytest.mark.parametrize('env, strict, validate', [
        ({'test': {'key': 'val'}}, False, None),
        ({'test': {'key': 'val'}}, True, False),
        ({'dev': {'key': 'val'}}, False, None),
        ({'dev': {'key': 'val'}}, True, False),
        ({}, False, None),
        ({}, True, False),
        ({'test': 'something'}, False, None),
        ({'test': 'something'}, True, False),
        ({'test': ['something']}, False, None),
        ({'test': ['something']}, True, False)
    ])
    @patch(MODULE + '.validate_environment')
    def test_should_skip(self, mock_validate, env, strict, validate,
                         fx_deployments, monkeypatch, runway_context):
        """Test should_skip."""
        mock_validate.return_value = validate
        env_copy = env.copy()
        payload = {'environment': env_copy.get('test', {}),
                   'environments': env_copy,
                   'parameters': {}}
        monkeypatch.setattr(Module, 'payload', payload)
        mod = Module(context=runway_context,
                     definition=fx_deployments.load('min_required').modules[0],
                     future=FutureDefinition(strict_environments=strict))

        result = mod.should_skip
        # assert not result
        if isinstance(env.get('test', {}), dict) and not strict:
            assert result is False
            mock_validate.assert_not_called()
            assert mod.payload['parameters'] == env.get('test', {})
            assert mod.payload['environment'] == (True if env.get('test') else {})
        else:
            assert result is (bool(not validate) if isinstance(validate, bool)
                              else False)
            mock_validate.assert_called_once_with(mod.ctx, mod, env,
                                                  strict=strict)

    @patch(MODULE + '.ModulePath')
    @patch(MODULE + '.RunwayModuleType')
    def test_type(self, mock_type, mock_path, fx_deployments, monkeypatch,
                  runway_context):
        """Test type."""
        mock_type.return_value = mock_type
        mock_path.module_root = 'path'
        monkeypatch.setattr(Module, 'path', mock_path)

        mod = Module(context=runway_context,
                     definition=fx_deployments.load('min_required').modules[0])
        monkeypatch.setattr(mod, 'payload', {})

        assert mod.type == mock_type
        mock_type.assert_called_once_with(path='path',
                                          class_path=None,
                                          type_str=None)
        del mod.type

        mod.payload.update({'class_path': 'parent.dir.class'})
        assert mod.type == mock_type
        mock_type.assert_called_with(path='path',
                                     class_path='parent.dir.class',
                                     type_str=None)
        del mod.type

        mod.payload.update({'type': 'test-type'})
        assert mod.type == mock_type
        mock_type.assert_called_with(path='path',
                                     class_path='parent.dir.class',
                                     type_str='test-type')
        del mod.type

    @pytest.mark.parametrize('config, use_concurrent, expected', [
        ('min_required', True, False),
        ('min_required', False, False),
        ('simple_parallel_module', True, True),
        ('simple_parallel_module', False, False)
    ])
    def test_use_async(self, config, use_concurrent, expected,
                       fx_deployments, runway_context):
        """Test use_async."""
        obj = Module(context=runway_context,
                     definition=fx_deployments.load(config).modules[0])
        obj.ctx._use_concurrent = use_concurrent
        assert obj.use_async == expected

    def test_deploy(self, fx_deployments, monkeypatch, runway_context):
        """Test deploy."""
        mock_run = MagicMock()
        monkeypatch.setattr(Module, 'run', mock_run)
        mod = Module(context=runway_context,
                     definition=fx_deployments.load('min_required').modules[0])
        assert mod.deploy()
        mock_run.assert_called_once_with('deploy')

    @patch(MODULE + '.concurrent.futures')
    @pytest.mark.skipif(sys.version_info.major < 3,
                        reason='only supported by python 3')
    def test_deploy_async(self, mock_futures, caplog, fx_deployments, monkeypatch,
                          runway_context):
        """Test deploy async."""
        caplog.set_level(logging.INFO, logger='runway')
        executor = MagicMock()
        mock_futures.ProcessPoolExecutor.return_value = executor
        monkeypatch.setattr(Module, 'use_async', True)

        obj = Module(context=runway_context,
                     definition=fx_deployments.load('simple_parallel_module').modules[0])
        assert not obj.deploy()
        assert 'Processing modules in parallel (output will be interwoven)' in \
            caplog.messages
        mock_futures.ProcessPoolExecutor.assert_called_once_with(
            max_workers=runway_context.env.max_concurrent_modules
        )
        executor.submit.assert_has_calls([
            call(obj.child_modules[0].run, 'deploy'),
            call(obj.child_modules[1].run, 'deploy')
        ])
        mock_futures.wait.assert_called_once()
        assert executor.submit.return_value.result.call_count == 2

    def test_deploy_sync(self, caplog, fx_deployments, monkeypatch,
                         runway_context):
        """Test deploy sync."""
        caplog.set_level(logging.INFO, logger='runway')
        mock_run = MagicMock()
        monkeypatch.setattr(Module, 'use_async', False)
        monkeypatch.setattr(Module, 'run', mock_run)

        mod = Module(context=runway_context,
                     definition=fx_deployments.load('simple_parallel_module').modules[0])
        assert not mod.deploy()
        assert 'Processing modules sequentially' in caplog.messages
        mock_run.assert_has_calls([call('deploy'), call('deploy')])

    @patch(MODULE + '.change_dir')
    def test_run(self, mock_change_dir, fx_deployments, monkeypatch,
                 runway_context, tmp_path):
        """Test run."""
        mock_type = MagicMock()
        mock_inst = MagicMock()
        mock_inst.deploy = MagicMock()
        mock_type.module_class.return_value = mock_inst
        monkeypatch.setattr(Module, 'should_skip', True)
        monkeypatch.setattr(Module, 'path', MagicMock(module_root=str(tmp_path)))
        monkeypatch.setattr(Module, 'type', mock_type)

        mod = Module(context=runway_context,
                     definition=fx_deployments.load('min_required').modules[0])
        assert not mod.run('deploy')
        mock_change_dir.assert_not_called()

        monkeypatch.setattr(Module, 'should_skip', False)
        assert not mod.run('deploy')
        mock_change_dir.assert_called_once_with(str(tmp_path))
        mock_type.module_class.assert_called_once_with(context=mod.ctx,
                                                       path=str(tmp_path),
                                                       options=mod.payload)
        mock_inst['deploy'].assert_called_once_with()

        del mock_inst.deploy
        with pytest.raises(SystemExit) as excinfo:
            assert mod.run('deploy')
        assert excinfo.value.code == 1

    def test_run_list(self, fx_deployments, monkeypatch, runway_context):
        """Test run_list."""
        mock_deploy = MagicMock()

        monkeypatch.setattr(Module, 'deploy', mock_deploy)
        assert not Module.run_list(
            action='deploy',
            context=runway_context,
            modules=fx_deployments.load('simple_parallel_module').modules,
            variables=MagicMock(),
            deployment=MagicMock(),
            future=MagicMock()
        )
        assert mock_deploy.call_count == 2
