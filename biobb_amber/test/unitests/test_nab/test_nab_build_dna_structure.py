from biobb_common.tools import test_fixtures as fx
from biobb_amber.nab.nab_build_dna_structure import NabBuildDNAStructure

class TestNabBuildDNAStructure():
    def setUp(self):
        fx.test_setup(self, 'nab_build_dna_structure')

    def tearDown(self):
        fx.test_teardown(self)
        pass

    def test_NabBuildDNAStructure(self):
        returncode= NabBuildDNAStructure(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])
        assert fx.exe_success(returncode)
