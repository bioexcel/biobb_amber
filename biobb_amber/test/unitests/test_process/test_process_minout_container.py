from biobb_common.tools import test_fixtures as fx
from biobb_amber.process.process_minout import process_minout

class TestProcessMinOutDocker():
    def setup_class(self):
        fx.test_setup(self, 'process_minout_docker')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_process_minout_docker(self):
        process_minout(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_dat_path'])
        assert fx.equal(self.paths['output_dat_path'], self.paths['ref_output_dat_path'])

import pytest
@pytest.mark.skip(reason="singularity currently not available")
class TestProcessMinOutSingularity():
    def setup_class(self):
        fx.test_setup(self, 'process_minout_singularity')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_process_minout_singularity(self):
        process_minout(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_dat_path'])
        assert fx.equal(self.paths['output_dat_path'], self.paths['ref_output_dat_path'])
