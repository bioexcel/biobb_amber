from biobb_common.tools import test_fixtures as fx
from biobb_amber.sander.sander_mdrun import sander_mdrun

class TestSanderMDRunDocker():
    def setup_class(self):
        fx.test_setup(self, 'sander_mdrun_docker')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_sander_mdrun_docker(self):
        sander_mdrun(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_log_path'])
        assert fx.not_empty(self.paths['output_rst_path'])
        assert fx.not_empty(self.paths['output_traj_path'])
        #assert fx.equal(self.paths['output_traj_path'], self.paths['ref_output_traj_path'])
        #assert fx.equal(self.paths['output_rst_path'], self.paths['ref_output_rst_path'])

import pytest
@pytest.mark.skip(reason="singularity currently not available")
class TestSanderMDRunSingularity():
    def setup_class(self):
        fx.test_setup(self, 'sander_mdrun_singularity')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_sander_mdrun_singularity(self):
        sander_mdrun(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_log_path'])
        assert fx.not_empty(self.paths['output_rst_path'])
        assert fx.not_empty(self.paths['output_traj_path'])
        #assert fx.equal(self.paths['output_traj_path'], self.paths['ref_output_traj_path'])
        #assert fx.equal(self.paths['output_rst_path'], self.paths['ref_output_rst_path'])


