from biobb_common.tools import test_fixtures as fx
from biobb_amber.ambpdb.amber_to_pdb import amber_to_pdb
import pytest


class TestAmberToPDBDocker():
    def setup_class(self):
        fx.test_setup(self, 'amber_to_pdb_docker')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_amber_to_pdb_docker(self):
        amber_to_pdb(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])


@pytest.mark.skip(reason="singularity currently not available")
class TestAmberToPDBSingularity():
    def setup_class(self):
        fx.test_setup(self, 'amber_to_pdb_docker_singularity')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_amber_to_pdb_docker_singularity(self):
        amber_to_pdb(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])
