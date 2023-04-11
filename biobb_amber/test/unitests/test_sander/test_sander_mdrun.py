from biobb_common.tools import test_fixtures as fx
from biobb_amber.sander.sander_mdrun import sander_mdrun


class TestSanderMDRun():
    def setup_class(self):
        fx.test_setup(self, 'sander_mdrun')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_sander_mdrun(self):
        sander_mdrun(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_log_path'])
        assert fx.not_empty(self.paths['output_rst_path'])
        assert fx.not_empty(self.paths['output_traj_path'])
        # assert fx.equal(self.paths['output_traj_path'], self.paths['ref_output_traj_path'])
        # assert fx.equal(self.paths['output_rst_path'], self.paths['ref_output_rst_path'])


class TestSanderMDRunDirectMDin():
    def setup_class(self):
        fx.test_setup(self, 'sander_mdrun_direct_mdin')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_sander_mdrun(self):
        sander_mdrun(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_log_path'])
        assert fx.not_empty(self.paths['output_rst_path'])
        assert fx.not_empty(self.paths['output_traj_path'])
        # assert fx.equal(self.paths['output_traj_path'], self.paths['ref_output_traj_path'])
        # assert fx.equal(self.paths['output_rst_path'], self.paths['ref_output_rst_path'])
