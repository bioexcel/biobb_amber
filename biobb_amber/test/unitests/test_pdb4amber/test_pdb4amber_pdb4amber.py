from biobb_common.tools import test_fixtures as fx
from biobb_amber.pdb4amber.pdb4amber import Pdb4amber

class TestPdb4amber():
    def setUp(self):
        fx.test_setup(self, 'pdb4amber')

    def tearDown(self):
        fx.test_teardown(self)
        pass

    def test_Pdb4amber(self):
        returncode= Pdb4amber(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])
        assert fx.exe_success(returncode)
