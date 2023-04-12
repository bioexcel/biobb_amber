from biobb_common.tools import test_fixtures as fx
from biobb_amber.cpptraj.cpptraj_randomize_ions import cpptraj_randomize_ions
import pytest


class TestCpptrajRandomizeIonsDocker():
    def setup_class(self):
        fx.test_setup(self, 'cpptraj_randomize_ions_docker')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_cpptraj_randomize_ions_docker(self):
        cpptraj_randomize_ions(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.not_empty(self.paths['output_crd_path'])
        # assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])
        # assert fx.equal(self.paths['output_crd_path'], self.paths['ref_output_crd_path'])


@pytest.mark.skip(reason="singularity currently not available")
class TestCpptrajRandomizeIonsSingularity():
    def setup_class(self):
        fx.test_setup(self, 'cpptraj_randomize_ions_singularity')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_cpptraj_randomize_ions_singularity(self):
        cpptraj_randomize_ions(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.not_empty(self.paths['output_crd_path'])
        # assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])
        # assert fx.equal(self.paths['output_crd_path'], self.paths['ref_output_crd_path'])
