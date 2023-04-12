from biobb_common.tools import test_fixtures as fx
from biobb_amber.leap.leap_build_linear_structure import leap_build_linear_structure
import pytest


class TestLeapBuildLinearStructureDocker():
    def setup_class(self):
        fx.test_setup(self, 'leap_build_linear_structure_docker')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_leap_build_linear_structure_docker(self):
        leap_build_linear_structure(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])


@pytest.mark.skip(reason="singularity currently not available")
class TestLeapBuildLinearStructureSingularity():
    def setup_class(self):
        fx.test_setup(self, 'leap_build_linear_structure_singularity')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_leap_build_linear_structure_singularity(self):
        leap_build_linear_structure(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])
