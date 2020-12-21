from biobb_common.tools import test_fixtures as fx
from biobb_amber.leap.leap_gen_top import LeapGenTop

class TestLeapGenTop():
    def setUp(self):
        fx.test_setup(self, 'leap_gen_top')

    def tearDown(self):
        fx.test_teardown(self)
        pass

    def test_LeapGenTop(self):
        returncode= LeapGenTop(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.not_empty(self.paths['output_top_path'])
        assert fx.not_empty(self.paths['output_crd_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])
        assert fx.equal(self.paths['output_top_path'], self.paths['ref_output_top_path'])
        assert fx.equal(self.paths['output_crd_path'], self.paths['ref_output_crd_path'])
        assert fx.exe_success(returncode)
