from biobb_common.tools import test_fixtures as fx
from biobb_amber.cphstats.cphstats_run import cphstats_run

class TestCphstatsRunDocker():
    def setup_class(self):
        fx.test_setup(self, 'cphstats_run_docker')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_cphstats_run_docker(self):
        cphstats_run(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_dat_path'])
        assert fx.equal(self.paths['output_dat_path'], self.paths['ref_output_dat_path'])

import pytest
@pytest.mark.skip(reason="singularity currently not available")
class TestCphstatsRunSingularity():
    def setup_class(self):
        fx.test_setup(self, 'cphstats_run_singularity')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_cphstats_run_singularity(self):
        cphstats_run(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_dat_path'])
        assert fx.equal(self.paths['output_dat_path'], self.paths['ref_output_dat_path'])