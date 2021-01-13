from biobb_common.tools import test_fixtures as fx
from biobb_amber.parmed.parmed_hmassrepartition import parmed_hmassrepartition

class TestParmedHMassRepartition():
    def setUp(self):
        fx.test_setup(self, 'parmed_hmassrepartition')

    def tearDown(self):
        fx.test_teardown(self)
        pass

    def test_parmed_hmassrepartition(self):
        parmed_hmassrepartition(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_top_path'])
        assert fx.equal(self.paths['output_top_path'], self.paths['ref_output_top_path'])
