from biobb_common.tools import test_fixtures as fx
from biobb_amber.parmed.parmed_hmassrepartition import parmed_hmassrepartition
import pytest


class TestParmedHMassRepartitionDocker():
    def setup_class(self):
        fx.test_setup(self, 'parmed_hmassrepartition_docker')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_parmed_hmassrepartition_docker(self):
        parmed_hmassrepartition(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_top_path'])
        assert fx.equal(self.paths['output_top_path'], self.paths['ref_output_top_path'])


@pytest.mark.skip(reason="singularity currently not available")
class TestParmedHMassRepartitionSingularity():
    def setup_class(self):
        fx.test_setup(self, 'parmed_hmassrepartition_singularity')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_parmed_hmassrepartition_singularity(self):
        parmed_hmassrepartition(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_top_path'])
        assert fx.equal(self.paths['output_top_path'], self.paths['ref_output_top_path'])
