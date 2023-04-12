from biobb_common.tools import test_fixtures as fx
from biobb_amber.pdb4amber.pdb4amber_run import pdb4amber_run
import pytest


class TestPdb4amberRunDocker():
    def setup_class(self):
        fx.test_setup(self, 'pdb4amber_run_docker')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_pdb4amber_run_docker(self):
        pdb4amber_run(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])


@pytest.mark.skip(reason="singularity currently not available")
class TestPdb4amberRunSingularity():
    def setup_class(self):
        fx.test_setup(self, 'pdb4amber_run_singularity')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_pdb4amber_run_singularity(self):
        pdb4amber_run(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])