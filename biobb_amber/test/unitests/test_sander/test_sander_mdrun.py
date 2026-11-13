# type: ignore
import re
from pathlib import Path
from biobb_common.tools import test_fixtures as fx
from biobb_amber.sander.sander_mdrun import SanderMDRun, sander_mdrun


class TestSanderMDRunParameterFiles():
    # The mdin is written without executing sander (provenance of the executions skipped by restart)
    def setup_class(self):
        fx.test_setup(self, 'sander_mdrun')

    def teardown_class(self):
        fx.test_teardown(self)

    def test_write_parameter_files(self, tmp_path):
        paths = {k: v for k, v in self.paths.items() if not k.startswith('ref_')}
        mdin_path, = SanderMDRun(properties=self.properties, **paths).write_parameter_files(str(tmp_path))
        assert Path(mdin_path) == tmp_path / 'sander.mdin'
        mdin = Path(mdin_path).read_text()
        assert re.search(r"imin = 1", mdin) and re.search(r"maxcyc = 500", mdin)

    def test_write_parameter_files_input_mdin(self, tmp_path):
        # Nothing is staged when the execution is skipped: the input mdin is read from its path
        input_mdin_path = str(Path(self.paths['input_top_path']).parent / 'min.mdin')
        paths = {k: v for k, v in self.paths.items() if not k.startswith('ref_')}
        mdin_path, = SanderMDRun(properties=self.properties, input_mdin_path=input_mdin_path, **paths).write_parameter_files(str(tmp_path))
        mdin = Path(mdin_path).read_text()
        assert f"Mdin read from input file: {input_mdin_path}" in mdin and re.search(r"maxcyc = 500", mdin)


class TestSanderMDRun():
    def setup_class(self):
        fx.test_setup(self, 'sander_mdrun')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_sander_mdrun(self):
        sander_mdrun(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_log_path'])
        assert fx.not_empty(self.paths['output_rst_path'])
        assert fx.not_empty(self.paths['output_traj_path'])
        # assert fx.equal(self.paths['output_traj_path'], self.paths['ref_output_traj_path'])
        # assert fx.equal(self.paths['output_rst_path'], self.paths['ref_output_rst_path'])


class TestSanderMDRunDirectMDin():
    def setup_class(self):
        fx.test_setup(self, 'sander_mdrun_direct_mdin')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_sander_mdrun(self):
        sander_mdrun(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_log_path'])
        assert fx.not_empty(self.paths['output_rst_path'])
        assert fx.not_empty(self.paths['output_traj_path'])
        # assert fx.equal(self.paths['output_traj_path'], self.paths['ref_output_traj_path'])
        # assert fx.equal(self.paths['output_rst_path'], self.paths['ref_output_rst_path'])
