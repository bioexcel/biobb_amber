from biobb_common.tools import test_fixtures as fx
from biobb_amber.pmemd.pmemd_mdrun import pmemd_mdrun


class TestPmemdMDRun():
    def setup_class(self):
        fx.test_setup(self, 'pmemd_mdrun')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_PmemdMDRun(self):
        pmemd_mdrun(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_log_path'])
        assert fx.not_empty(self.paths['output_rst_path'])
        assert fx.not_empty(self.paths['output_traj_path'])
        # assert fx.equal(self.paths['output_traj_path'], self.paths['ref_output_traj_path'])
        # assert fx.equal(self.paths['output_rst_path'], self.paths['ref_output_rst_path'])
