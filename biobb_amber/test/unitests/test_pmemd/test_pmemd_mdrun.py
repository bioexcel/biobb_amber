# type: ignore
import re
from pathlib import Path
from biobb_common.tools import test_fixtures as fx
from biobb_amber.pmemd.pmemd_mdrun import PmemdMDRun, pmemd_mdrun


class TestPmemdMDRunParameterFiles():
    # The mdin is written without executing pmemd (provenance of the executions skipped by restart)
    def setup_class(self):
        fx.test_setup(self, 'pmemd_mdrun')

    def teardown_class(self):
        fx.test_teardown(self)

    def test_write_parameter_files(self, tmp_path):
        paths = {k: v for k, v in self.paths.items() if not k.startswith('ref_')}
        mdin_path, = PmemdMDRun(properties=self.properties, **paths).write_parameter_files(str(tmp_path))
        assert Path(mdin_path) == tmp_path / 'pmemd.mdin'
        mdin = Path(mdin_path).read_text()
        assert re.search(r"imin = 1", mdin) and re.search(r"maxcyc = 500", mdin)


class TestPmemdMDRun():
    def setup_class(self):
        fx.test_setup(self, 'pmemd_mdrun')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_PmemdMDRun(self):
        pmemd_mdrun(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_log_path'])
        assert fx.not_empty(self.paths['output_rst_path'])
        assert fx.not_empty(self.paths['output_traj_path'])
        # assert fx.equal(self.paths['output_traj_path'], self.paths['ref_output_traj_path'])
        # assert fx.equal(self.paths['output_rst_path'], self.paths['ref_output_rst_path'])
