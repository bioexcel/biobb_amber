# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_amber.process.process_mdout import process_mdout


class TestProcessMDOut():
    def setup_class(self):
        fx.test_setup(self, 'process_mdout')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_process_mdout(self):
        process_mdout(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_dat_path'])
        assert fx.equal(self.paths['output_dat_path'], self.paths['ref_output_dat_path'])
