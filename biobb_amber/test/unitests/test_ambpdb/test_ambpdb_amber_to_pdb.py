from biobb_common.tools import test_fixtures as fx
from biobb_amber.ambpdb.amber_to_pdb import AmberToPDB

class TestAmberToPDB():
    def setUp(self):
        fx.test_setup(self, 'amber_to_pdb')

    def tearDown(self):
        fx.test_teardown(self)
        pass

    def test_AmberToPDB(self):
        returncode= AmberToPDB(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])
        assert fx.exe_success(returncode)
