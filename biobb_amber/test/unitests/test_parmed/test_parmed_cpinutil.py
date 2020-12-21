from biobb_common.tools import test_fixtures as fx
from biobb_amber.parmed.parmed_cpinutil import ParmedCpinutil

class TestParmedCpinutil():
    def setUp(self):
        fx.test_setup(self, 'parmed_cpinutil')

    def tearDown(self):
        fx.test_teardown(self)
        pass

    def test_ParmedCpinutil(self):
        returncode= ParmedCpinutil(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_cpin_path'])
        assert fx.equal(self.paths['output_cpin_path'], self.paths['ref_output_cpin_path'])
        assert fx.exe_success(returncode)
