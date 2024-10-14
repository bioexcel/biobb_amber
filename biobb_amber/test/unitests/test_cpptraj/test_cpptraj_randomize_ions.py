# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_amber.cpptraj.cpptraj_randomize_ions import cpptraj_randomize_ions


class TestCpptrajRandomizeIons():
    def setup_class(self):
        fx.test_setup(self, 'cpptraj_randomize_ions')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_cpptraj_randomize_ions(self):
        cpptraj_randomize_ions(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.not_empty(self.paths['output_crd_path'])
        # assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])
        # assert fx.equal(self.paths['output_crd_path'], self.paths['ref_output_crd_path'])
