from biobb_common.tools import test_fixtures as fx
from biobb_amber.leap.leap_solvate import leap_solvate
import pytest


class TestLeapSolvateDocker():
    def setup_class(self):
        fx.test_setup(self, 'leap_solvate_docker')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_leap_solvate_docker(self):
        leap_solvate(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.not_empty(self.paths['output_top_path'])
        assert fx.not_empty(self.paths['output_crd_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])
        # assert fx.equal(self.paths['output_top_path'], self.paths['ref_output_top_path'])
        assert fx.equal(self.paths['output_crd_path'], self.paths['ref_output_crd_path'])


@pytest.mark.skip(reason="singularity currently not available")
class TestLeapSolvateSingularity():
    def setup_class(self):
        fx.test_setup(self, 'leap_solvate_singularity')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_leap_solvate_singularity(self):
        leap_solvate(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.not_empty(self.paths['output_top_path'])
        assert fx.not_empty(self.paths['output_crd_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])
        # assert fx.equal(self.paths['output_top_path'], self.paths['ref_output_top_path'])
        assert fx.equal(self.paths['output_crd_path'], self.paths['ref_output_crd_path'])