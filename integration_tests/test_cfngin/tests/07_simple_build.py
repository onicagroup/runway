"""CFNgin test."""
# flake8: noqa
# pylint: disable=invalid-name
from os.path import basename

from integration_tests.test_cfngin.test_cfngin import Cfngin


class TestSimpleBuild(Cfngin):
    """Test CFNgin simple build.

    Requires valid AWS credentials.

    """

    REQUIRED_FIXTURE_FILES = [
        '.'.join(basename(__file__).split('.')[:-1]) + '.yaml'
    ]
    TEST_NAME = __name__

    def _build(self):
        """Execute and assert initial build."""
        code, _stdout, stderr = self.runway_cmd('deploy')
        assert code == 0, 'exit code should be zero'
        expected_lines = [
            'Using default AWS provider mode',
            'vpc: submitted (creating new stack)',
            'vpc: complete (creating new stack)'
        ]
        for line in expected_lines:
            assert line in stderr, '"{line}" missing from output'

    def _update_no_change(self):
        """Execute and assert second build with no changes."""
        code, _stdout, stderr = self.runway_cmd('deploy')
        assert code == 0, 'exit code should be zero'
        expected_lines = [
            'Using default AWS provider mode',
            'vpc: skipped (nochange)'
        ]
        for line in expected_lines:
            assert line in stderr, '"{line}" missing from output'

    def _destroy(self):
        """Execute and assert destroy."""
        code, _stdout, stderr = self.runway_cmd('destroy')
        assert code == 0, 'exit code should be zero'
        expected_lines = [
            'vpc: submitted (submitted for destruction)',
            'vpc: complete (stack destroyed)'
        ]
        for line in expected_lines:
            assert line in stderr, f'"{line}" missing from output'

    def run(self):
        """Run the test."""
        self.copy_fixtures()
        self._build()
        self._update_no_change()
        self._destroy()

    def teardown(self):
        """Teardown any created resources and delete files."""
        self.runway_cmd('destroy')  # cleanup incase of failure
        self.cleanup_fixtures()
