"""Test runway.env_mgr.tfenv."""
# pylint: disable=no-self-use
import json

import hcl
import pytest
import six
from mock import MagicMock, patch

from runway.env_mgr.tfenv import (TF_VERSION_FILENAME, TFEnvManager,
                                  get_available_tf_versions,
                                  get_latest_tf_version, get_version_requested)

MODULE = 'runway.env_mgr.tfenv'


@patch(MODULE + '.requests')
def test_get_available_tf_versions(mock_requests):
    """Test runway.env_mgr.tfenv.get_available_tf_versions."""
    response = {
        'terraform': {
            'versions': {
                '0.12.0': {},
                '0.12.0-beta': {}
            }
        }
    }
    mock_requests.get.return_value = MagicMock(text=json.dumps(response))
    assert get_available_tf_versions() == ['0.12.0']
    assert get_available_tf_versions(include_prerelease=True) == [
        '0.12.0-beta',
        '0.12.0'
    ]


@patch(MODULE + '.get_available_tf_versions')
def test_get_latest_tf_version(mock_get_available_tf_versions):
    """Test runway.env_mgr.tfenv.get_latest_tf_version."""
    mock_get_available_tf_versions.return_value = ['latest']
    assert get_latest_tf_version() == 'latest'
    mock_get_available_tf_versions.assert_called_once_with(False)
    assert get_latest_tf_version(include_prerelease=True) == 'latest'
    mock_get_available_tf_versions.assert_called_with(True)


def test_get_version_requested(tmp_path):
    """Test runway.env_mgr.tfenv.get_version_requested."""
    tf_version = tmp_path / TF_VERSION_FILENAME
    with pytest.raises(SystemExit) as excinfo:
        assert get_version_requested(tmp_path)
    assert excinfo.value.code == 1

    tf_version.write_text(six.u('0.12.0'))
    assert get_version_requested(tmp_path) == '0.12.0'


class TestTFEnvManager(object):
    """Test runway.env_mgr.tfenv.TFEnvManager."""

    def test_backend(self, monkeypatch, tmp_path):
        """Test backend."""
        monkeypatch.setattr(TFEnvManager, 'terraform_block', {
            'backend': {
                's3': {
                    'bucket': 'name'
                }
            }
        })
        tfenv = TFEnvManager(tmp_path)
        assert tfenv.backend == {
            'type': 's3',
            'config': {
                'bucket': 'name'
            }
        }

        del tfenv.backend
        monkeypatch.setattr(tfenv, 'terraform_block', {})
        assert tfenv.backend == {
            'type': None,
            'config': {}
        }

    def test_get_min_required(self, monkeypatch, tmp_path):
        """Test get_min_required."""
        monkeypatch.setattr(TFEnvManager, 'terraform_block', {})
        tfenv = TFEnvManager(tmp_path)

        with pytest.raises(SystemExit) as excinfo:
            assert tfenv.get_min_required()
        assert excinfo.value.code

        monkeypatch.setattr(tfenv, 'terraform_block', {
            'required_version': '!=0.12.0'
        })
        with pytest.raises(SystemExit) as excinfo:
            assert tfenv.get_min_required()
        assert excinfo.value.code

        monkeypatch.setattr(tfenv, 'terraform_block', {
            'required_version': '~>0.12.0'
        })
        assert tfenv.get_min_required() == '0.12.0'

    @patch(MODULE + '.get_available_tf_versions')
    @patch(MODULE + '.get_version_requested')
    @patch(MODULE + '.download_tf_release')
    def test_install(self, mock_download, mock_get_version_requested,
                     mock_available_versions, monkeypatch, tmp_path):
        """Test install."""
        mock_available_versions.return_value = ['0.12.0', '0.11.5']
        mock_get_version_requested.return_value = '0.11.5'
        monkeypatch.setattr(TFEnvManager, 'versions_dir', tmp_path)
        tfenv = TFEnvManager(tmp_path)

        assert tfenv.install('0.12.0')
        mock_available_versions.assert_called_once_with(True)
        mock_download.assert_called_once_with(
            '0.12.0', tfenv.versions_dir, tfenv.command_suffix
        )
        assert tfenv.current_version == '0.12.0'

        assert tfenv.install()
        mock_download.assert_called_with(
            '0.11.5', tfenv.versions_dir, tfenv.command_suffix
        )
        assert tfenv.current_version == '0.11.5'

    @patch(MODULE + '.get_available_tf_versions')
    @patch(MODULE + '.download_tf_release')
    def test_install_already_installed(self, mock_download,
                                       mock_available_versions,
                                       monkeypatch, tmp_path):
        """Test install with version already installed."""
        mock_available_versions.return_value = ['0.12.0']
        monkeypatch.setattr(TFEnvManager, 'versions_dir', tmp_path)
        tfenv = TFEnvManager(tmp_path)
        (tfenv.versions_dir / '0.12.0').mkdir()

        assert tfenv.install('0.12.0')
        mock_available_versions.assert_not_called()
        mock_download.assert_not_called()
        assert tfenv.current_version == '0.12.0'

        assert tfenv.install(r'0\.12\..*')  # regex does not match dir

    @patch(MODULE + '.get_available_tf_versions')
    @patch(MODULE + '.download_tf_release')
    def test_install_latest(self, mock_download, mock_available_versions,
                            monkeypatch, tmp_path):
        """Test install latest."""
        mock_available_versions.return_value = ['0.12.0', '0.11.5']
        monkeypatch.setattr(TFEnvManager, 'versions_dir', tmp_path)
        tfenv = TFEnvManager(tmp_path)

        assert tfenv.install('latest')
        mock_available_versions.assert_called_once_with(False)
        mock_download.assert_called_once_with(
            '0.12.0', tfenv.versions_dir, tfenv.command_suffix
        )
        assert tfenv.current_version == '0.12.0'

        assert tfenv.install('latest:0.11.5')
        mock_available_versions.assert_called_with(False)
        mock_download.assert_called_with(
            '0.11.5', tfenv.versions_dir, tfenv.command_suffix
        )
        assert tfenv.current_version == '0.11.5'

    @patch(MODULE + '.get_available_tf_versions')
    @patch(MODULE + '.download_tf_release')
    def test_install_min_required(self, mock_download, mock_available_versions,
                                  monkeypatch, tmp_path):
        """Test install min_required."""
        mock_available_versions.return_value = ['0.12.0']
        monkeypatch.setattr(TFEnvManager, 'versions_dir', tmp_path)
        monkeypatch.setattr(
            TFEnvManager, 'get_min_required', MagicMock(return_value='0.12.0')
        )
        tfenv = TFEnvManager(tmp_path)

        assert tfenv.install('min-required')
        mock_available_versions.assert_called_once_with(True)
        mock_download.assert_called_once_with(
            '0.12.0', tfenv.versions_dir, tfenv.command_suffix
        )
        assert tfenv.current_version == '0.12.0'
        tfenv.get_min_required.assert_called_once_with()  # pylint: disable=no-member

    @patch(MODULE + '.get_available_tf_versions')
    @patch(MODULE + '.download_tf_release')
    def test_install_unavailable(self, mock_download, mock_available_versions,
                                 monkeypatch, tmp_path):
        """Test install."""
        mock_available_versions.return_value = []
        monkeypatch.setattr(TFEnvManager, 'versions_dir', tmp_path)
        tfenv = TFEnvManager(tmp_path)

        with pytest.raises(SystemExit) as excinfo:
            assert tfenv.install('0.12.0')
        assert excinfo.value.code == 1
        mock_available_versions.assert_called_once_with(True)
        mock_download.assert_not_called()
        assert not tfenv.current_version

    def test_terraform_block(self, tmp_path):
        """Test terraform_block."""
        content = {
            'terraform': {
                'backend': {
                    's3': {
                        'bucket': 'name'
                    }
                }
            }
        }
        tf_file = tmp_path / 'module.tf'
        tf_file.write_text(six.u(hcl.dumps(content)))
        tfenv = TFEnvManager(tmp_path)

        assert tfenv.terraform_block == content['terraform']
