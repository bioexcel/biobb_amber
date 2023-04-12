from biobb_common.tools import test_fixtures as fx
from biobb_amber.cphstats.cestats_run import cestats_run


class TestCestatsRun():
    def setup_class(self):
        fx.test_setup(self, 'cestats_run')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_cestats_run(self):
        cestats_run(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_dat_path'])
        assert fx.equal(self.paths['output_dat_path'], self.paths['ref_output_dat_path'])
