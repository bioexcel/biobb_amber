from biobb_common.tools import test_fixtures as fx
from biobb_amber.leap.leap_add_ions import leap_add_ions
import pytest


class TestLeapAddIonsDocker():
    def setup_class(self):
        fx.test_setup(self, 'leap_add_ions_docker')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_leap_add_ions_docker(self):
        leap_add_ions(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.not_empty(self.paths['output_top_path'])
        assert fx.not_empty(self.paths['output_crd_path'])
        # assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])
        # assert fx.equal(self.paths['output_top_path'], self.paths['ref_output_top_path'])
        # assert fx.equal(self.paths['output_crd_path'], self.paths['ref_output_crd_path'])


@pytest.mark.skip(reason="singularity currently not available")
class TestLeapAddIonsSingularity():
    def setup_class(self):
        fx.test_setup(self, 'leap_add_ions_singularity')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_leap_add_ions_singularity(self):
        leap_add_ions(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.not_empty(self.paths['output_top_path'])
        assert fx.not_empty(self.paths['output_crd_path'])
        # assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])
        # assert fx.equal(self.paths['output_top_path'], self.paths['ref_output_top_path'])
        # assert fx.equal(self.paths['output_crd_path'], self.paths['ref_output_crd_path'])
