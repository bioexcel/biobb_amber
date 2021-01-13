from biobb_common.tools import test_fixtures as fx
from biobb_amber.parmed.parmed_hmassrepartition import ParmedHMassRepartition

class TestParmedHMassRepartition():
    def setUp(self):
        fx.test_setup(self, 'parmed_hmassrepartition')

    def tearDown(self):
        fx.test_teardown(self)
        pass

    def test_ParmedHMassRepartition(self):
        returncode= ParmedHMassRepartition(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_top_path'])
        assert fx.equal(self.paths['output_top_path'], self.paths['ref_output_top_path'])
        assert fx.exe_success(returncode)
