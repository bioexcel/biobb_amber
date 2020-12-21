from biobb_common.tools import test_fixtures as fx
from biobb_amber.leap.leap_build_linear_structure import LeapBuildLinearStructure

class TestLeapBuildLinearStructure():
    def setUp(self):
        fx.test_setup(self, 'leap_build_linear_structure')

    def tearDown(self):
        fx.test_teardown(self)
        pass

    def test_LeapBuildLinearStructure(self):
        returncode= LeapBuildLinearStructure(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])
        assert fx.exe_success(returncode)
