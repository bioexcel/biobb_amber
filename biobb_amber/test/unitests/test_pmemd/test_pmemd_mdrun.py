from biobb_common.tools import test_fixtures as fx
from biobb_amber.pmemd.pmemd_mdrun import PmemdMDRun

class TestPmemdMDRun():
    def setUp(self):
        fx.test_setup(self, 'pmemd_mdrun')

    def tearDown(self):
        fx.test_teardown(self)
        pass

    def test_PmemdMDRun(self):
        returncode= PmemdMDRun(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_log_path'])
        assert fx.not_empty(self.paths['output_rst_path'])
        assert fx.not_empty(self.paths['output_traj_path'])
        assert fx.equal(self.paths['output_traj_path'], self.paths['ref_output_traj_path'])
        assert fx.equal(self.paths['output_rst_path'], self.paths['ref_output_rst_path'])
        assert fx.exe_success(returncode)
