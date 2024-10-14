# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_amber.parmed.parmed_cpinutil import parmed_cpinutil
import pytest


class TestParmedCpinUtilDocker():
    def setup_class(self):
        fx.test_setup(self, 'parmed_cpinutil_docker')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_parmed_cpinutil_docker(self):
        parmed_cpinutil(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_cpin_path'])
        assert fx.equal(self.paths['output_cpin_path'], self.paths['ref_output_cpin_path'])


@pytest.mark.skip(reason="singularity currently not available")
class TestParmedCpinUtilSingularity():
    def setup_class(self):
        fx.test_setup(self, 'parmed_cpinutil_singularity')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_parmed_cpinutil_singularity(self):
        parmed_cpinutil(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_cpin_path'])
        assert fx.equal(self.paths['output_cpin_path'], self.paths['ref_output_cpin_path'])
