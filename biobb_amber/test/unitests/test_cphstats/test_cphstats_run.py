from biobb_common.tools import test_fixtures as fx
from biobb_amber.cphstats.cphstats_run import cphstats_run

class TestCphstatsRun():
    def setUp(self):
        fx.test_setup(self, 'cphstats_run')

    def tearDown(self):
        fx.test_teardown(self)
        pass

    def test_cphstats_run(self):
        cphstats_run(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_dat_path'])
        assert fx.equal(self.paths['output_dat_path'], self.paths['ref_output_dat_path'])
