from biobb_common.tools import test_fixtures as fx
from biobb_amber.parmed.parmed_cpinutil import parmed_cpinutil

class TestParmedCpinUtil():
    def setUp(self):
        fx.test_setup(self, 'parmed_cpinutil')

    def tearDown(self):
        fx.test_teardown(self)
        pass

    def test_parmed_cpinutil(self):
        parmed_cpinutil(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_cpin_path'])
        assert fx.equal(self.paths['output_cpin_path'], self.paths['ref_output_cpin_path'])
