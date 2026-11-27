#!/usr/bin/env python3

"""Module containing the PmemdMDRun class and the command line interface."""
from typing import Optional
from pathlib import Path
from biobb_common.generic.biobb_object import BiobbObject, launcher

from biobb_amber.sander.common import write_mdin


class PmemdMDRun(BiobbObject):
    """
    | biobb_amber PmemdMDRun
    | Wrapper of the `AmberTools (AMBER MD Package) pmemd tool <https://ambermd.org/AmberTools.php>`_ module.
    | Runs molecular dynamics using pmemd tool from the AMBER MD package.

    Args:
        input_top_path (str): Input topology file (AMBER ParmTop). File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pmemd/cln025.prmtop>`_. Accepted formats: top (edam:format_3881), parmtop (edam:format_3881), prmtop (edam:format_3881).
        input_crd_path (str): Input coordinates file (AMBER crd). File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pmemd/cln025.inpcrd>`_. Accepted formats: crd (edam:format_3878), mdcrd (edam:format_3878), inpcrd (edam:format_3878), rst (edam:format_3886), rst7 (edam:format_3886), netcdf (edam:format_3650), nc (edam:format_3650), ncrst (edam:format_3886).
        input_mdin_path (str) (Optional): Input configuration file (MD run options) (AMBER mdin). File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pmemd/npt.mdin>`_. Accepted formats: mdin (edam:format_2330), in (edam:format_2330), txt (edam:format_2330).
        input_cpin_path (str) (Optional): Input constant pH file (AMBER cpin). File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pmemd/cln025.cpin>`_. Accepted formats: cpin (edam:format_2330), in (edam:format_2330), txt (edam:format_2330).
        input_ref_path (str) (Optional): Input reference coordinates for position restraints. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pmemd/sander.rst>`_. Accepted formats:  crd (edam:format_3878), mdcrd (edam:format_3878), inpcrd (edam:format_3878), rst (edam:format_3886), rst7 (edam:format_3886), netcdf (edam:format_3650), nc (edam:format_3650), ncrst (edam:format_3886).
        output_log_path (str): Output log file. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/pmemd/sander.log>`_. Accepted formats: log (edam:format_2330), out (edam:format_2330), txt (edam:format_2330), o (edam:format_2330).
        output_traj_path (str): Output trajectory file. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/pmemd/sander.x>`_. Accepted formats: trj (edam:format_3878), crd (edam:format_3878), mdcrd (edam:format_3878), x (edam:format_3878), netcdf (edam:format_3650), nc (edam:format_3650).
        output_rst_path (str): Output restart file. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/pmemd/sander.rst>`_. Accepted formats: rst (edam:format_3886), rst7 (edam:format_3886), netcdf (edam:format_3650), nc (edam:format_3650), ncrst (edam:format_3886).
        output_cpout_path (str) (Optional): Output constant pH file (AMBER cpout). File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/pmemd/sander.cpout>`_. Accepted formats: cpout (edam:format_2330).
        output_cprst_path (str) (Optional): Output constant pH restart file (AMBER rstout). File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/pmemd/sander.cprst>`_. Accepted formats: cprst (edam:format_3886), rst (edam:format_3886), rst7 (edam:format_3886).
        output_mdinfo_path (str) (Optional): Output MD info. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/pmemd/sander.mdinfo>`_. Accepted formats: mdinfo (edam:format_2330).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **mdin** (*dict*) - ({}) pmemd MD run options specification. (Used if *input_mdin_path* is None)
            * **binary_path** (*str*) - ("pmemd") pmemd binary path to be used.
            * **simulation_type** (*str*) - ("minimization") Default options for the mdin file. Each creates a different mdin file. Values: `minimization <https://biobb-amber.readthedocs.io/en/latest/_static/mdins/min.mdin>`_ (Runs an energy minimization), `min_vacuo <https://biobb-amber.readthedocs.io/en/latest/_static/mdins/min_vacuo.mdin>`_ (Runs an energy minimization in vacuo), `NVT <https://biobb-amber.readthedocs.io/en/latest/_static/mdins/nvt.mdin>`_ (Runs an NVT equilibration), `npt <https://biobb-amber.readthedocs.io/en/latest/_static/mdins/npt.mdin>`_ (Runs an NPT equilibration), `free <https://biobb-amber.readthedocs.io/en/latest/_static/mdins/free.mdin>`_ (Runs a MD simulation), `heat <https://biobb-amber.readthedocs.io/en/latest/_static/mdins/heat.mdin>`_ (Heats the MD system).
            * **mpi_bin** (*str*) - (None) Path to the MPI runner. Usually "mpirun" or "srun".
            * **mpi_np** (*int*) - (None) [0~1000|1] Number of MPI processes. Usually an integer bigger than 1.
            * **mpi_flags** (*str*) - (None) Path to the MPI hostlist file.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_amber.pmemd.pmemd_mdrun import pmemd_mdrun
            prop = {
                'simulation_type' : 'npt',
                'mdin' : {
                    'dt' : 0.002
                }
            }
            pmemd_mdrun(input_top_path='/path/to/topology.top',
                         input_crd_path='/path/to/coordinates.crd',
                         output_traj_path='/path/to/newTrajectory.crd',
                         output_rst_path='/path/to/newRestart.rst',
                         output_log_path='/path/to/newAmberlog.log',
                         properties=prop)

    Info:
        * wrapped_software:
            * name: AMBER pmemd
            * version: >20
            * license: other
            * multinode: mpi
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, input_top_path: str, input_crd_path: str, output_log_path: str, output_traj_path: str, output_rst_path: str,
                 input_ref_path: Optional[str] = None, input_mdin_path: Optional[str] = None, input_cpin_path: Optional[str] = None, output_cpout_path: Optional[str] = None, output_cprst_path: Optional[str] = None, output_mdinfo_path: Optional[str] = None,
                 properties: Optional[dict] = None, **kwargs) -> None:
        super().__init__(**locals())

    def create_mdin(self, path: Optional[str] = None) -> str:
        """Creates an AMBER MD configuration file (mdin) using the properties file settings"""
        return write_mdin(str(path), self.io_dict['in']['input_mdin_path'], self.mdin, self.simulation_type)

    def run(self):
        """Launches the execution of the PmemdMDRun module."""

        # Pmemd configuration (instructions) file, in the sandbox
        self.output_mdin_path = self.staged_path(self.create_mdin(path=self.create_tmp_file("_pmemd.mdin")))

        # Command line
        # pmemd -O -i mdin/min.mdin -p $1.cpH.prmtop -c ph$i/$1.inpcrd -r ph$i/$1.min.rst7 -o ph$i/$1.min.o
        self.cmd = [self.binary_path,
                    '-O',
                    '-i', self.output_mdin_path,
                    '-p', self.stage_io_dict['in']['input_top_path'],
                    '-c', self.stage_io_dict['in']['input_crd_path'],
                    '-r', self.stage_io_dict['out']['output_rst_path'],
                    '-o', self.stage_io_dict['out']['output_log_path'],
                    '-x', self.stage_io_dict['out']['output_traj_path']
                    ]

        if self.stage_io_dict['in'].get('input_ref_path'):
            self.cmd.append('-ref')
            self.cmd.append(self.stage_io_dict['in']['input_ref_path'])

        if self.stage_io_dict['in'].get('input_cpin_path'):
            self.cmd.append('-cpin')
            self.cmd.append(self.stage_io_dict['in']['input_cpin_path'])

        if self.stage_io_dict['out'].get('output_mdinfo_path'):
            self.cmd.append('-inf')
            self.cmd.append(self.stage_io_dict['out']['output_mdinfo_path'])

        if self.stage_io_dict['out'].get('output_cpout_path'):
            self.cmd.append('-cpout')
            self.cmd.append(self.stage_io_dict['out']['output_cpout_path'])

        if self.stage_io_dict['out'].get('output_cprst_path'):
            self.cmd.append('-cprestrt')
            self.cmd.append(self.stage_io_dict['out']['output_cprst_path'])

        # general mpi properties
        if self.mpi_bin:
            mpi_cmd = [self.mpi_bin]
            if self.mpi_np:
                mpi_cmd.append('-n')
                mpi_cmd.append(str(self.mpi_np))
            if self.mpi_flags:
                mpi_cmd.append(self.mpi_flags)
            self.cmd = mpi_cmd + self.cmd

        # Run Biobb block
        self.run_biobb()

    def write_parameter_files(self, directory: str) -> list[str]:
        """Write the mdin file to **directory** without executing pmemd, used by the
        provenance of the executions skipped by the restart property."""
        return [self.create_mdin(path=str(Path(directory).joinpath("pmemd.mdin")))]


pmemd_mdrun = launcher(PmemdMDRun)

if __name__ == '__main__':
    PmemdMDRun.main()
