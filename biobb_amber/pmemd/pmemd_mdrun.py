#!/usr/bin/env python3

"""Module containing the PmemdMDRun class and the command line interface."""
import argparse
import shutil, re
from pathlib import Path, PurePath
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_amber.pmemd.common import *

class PmemdMDRun():
    """
    | biobb_amber PmemdMDRun
    | Wrapper of the `AmberTools (AMBER MD Package) pmemd tool <https://ambermd.org/AmberTools.php>`_ module.
    | Runs molecular dynamics using pmemd tool from the AMBER MD package.

    Args:
        input_top_path (str): Input topology file (AMBER ParmTop). File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pmemd/structure.top>`_. Accepted formats: top (edam:format_3881), parmtop (edam:format_3881), prmtop (edam:format_3881).
        input_crd_path (str): Input coordinates file (AMBER crd). File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pmemd/structure.crd>`_. Accepted formats: crd (edam:format_3878), mdcrd (edam:format_3878), inpcrd (edam:format_3878).
        input_mdin_path (str) (Optional): Input configuration file (MD run options) (AMBER mdin). File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pmemd/pmemd.mdin>`_. Accepted formats: mdin (edam:format_2330), in (edam:format_2330), txt (edam:format_2330).
        input_cpin_path (str) (Optional): Input constant pH file (AMBER cpin). File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pmemd/pmemd.cpin>`_. Accepted formats: cpin (edam:format_2330).
        input_ref_path (str) (Optional): Input reference coordinates for position restraints. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pmemd/pmemd.refc>`_. Accepted formats: rst (edam:format_3886), rst7 (edam:format_3886).
        output_log_path (str): Output log file. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pmemd/md.out>`_. Accepted formats: log (edam:format_2330), out (edam:format_2330), txt (edam:format_2330), o (edam:format_2330).
        output_traj_path (str): Output trajectory file. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pmemd/md.x>`_. Accepted formats: trj (edam:format_3878), crd (edam:format_3878), mdcrd (edam:format_3878), x (edam:format_3878), netcdf (edam:format_3650), nc (edam:format_3650).
        output_rst_path (str): Output restart file. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pmemd/md.rst>`_. Accepted formats: rst (edam:format_3886), rst7 (edam:format_3886).
        output_cpout_path (str) (Optional): Output constant pH file (AMBER cpout). File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pmemd/pmemd.cpout>`_. Accepted formats: cpout (edam:format_2330).
        output_cprst_path (str) (Optional): Output constant pH restart file (AMBER rstout). File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pmemd/pmemd.cprst>`_. Accepted formats: cprst (edam:format_3886), rst (edam:format_3886), rst7 (edam:format_3886).
        output_mdinfo_path (str) (Optional): Output MD info. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pmemd/pmemd.mdinfo>`_. Accepted formats: mdinfo (edam:format_2330).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **mdin** (*dict*) - ({}) pmemd MD run options specification. (Used if *input_mdin_path* is None)
            * **pmemd_path** (*str*) - ("pmemd") pmemd binary path to be used.
            * **simulation_type** (*str*) - ("minimization") Default options for the mdin file. Each creates a different mdin file. Values: `minimization <https://biobb-amber.readthedocs.io/en/latest/_static/mdin/minimization.mdin>`_ (Runs an energy minimization), `min_vacuo <https://biobb-amber.readthedocs.io/en/latest/_static/mdin/min_vacuo.mdin>`_ (Runs an energy minimization in vacuo), `NVT <https://biobb-amber.readthedocs.io/en/latest/_static/mdin/NVT.mdin>`_ (Runs an NVT equilibration), `npt <https://biobb-amber.readthedocs.io/en/latest/_static/mdin/NPT.mdin>`_ (Runs an NPT equilibration), `free <https://biobb-amber.readthedocs.io/en/latest/_static/mdin/free.mdin>`_ (Runs a MD simulation).
            * **mpi_bin** (*str*) - (None) Path to the MPI runner. Usually "mpirun" or "srun".
            * **mpi_np** (*int*) - (0) [0~1000|1] Number of MPI processes. Usually an integer bigger than 1.
            * **mpi_hostlist** (*str*) - (None) Path to the MPI hostlist file.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

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
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """
    def __init__(self, input_top_path: str, input_crd_path: str, output_log_path: str, output_traj_path: str, output_rst_path: str,
                 input_ref_path: str = None, input_mdin_path: str = None, input_cpin_path: str = None, output_cpout_path: str = None, output_cprst_path: str = None, output_mdinfo_path: str = None,
                 properties: dict = None, **kwargs) -> None:
        properties = properties or {}

        # Input/Output files
        self.io_dict = {
            'in': { 'input_top_path': input_top_path,
                    'input_crd_path': input_crd_path,
                    'input_mdin_path': input_mdin_path,
                    'input_ref_path': input_ref_path,
                    'input_cpin_path': input_cpin_path },
            'out': {    'output_log_path': output_log_path,
                        'output_traj_path': output_traj_path,
                        'output_rst_path': output_rst_path,
                        'output_cpout_path': output_cpout_path,
                        'output_cprst_path': output_cprst_path,
                        'output_mdinfo_path': output_mdinfo_path }
        }

        # Properties specific for BB
        self.properties = properties
        self.simulation_type = properties.get('simulation_type', "minimization")
        self.pmemd_path = properties.get('pmemd_path', "pmemd")
        self.mdin = {k: str(v) for k, v in properties.get('mdin', dict()).items()}

        # Properties for MPI
        self.mpi_bin = properties.get('mpi_bin')
        self.mpi_np = properties.get('mpi_np')
        self.mpi_hostlist = properties.get('mpi_hostlist')

        # Properties common in all BB
        self.can_write_console_log = properties.get('can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')
        self.remove_tmp = properties.get('remove_tmp', True)
        self.restart = properties.get('restart', False)

    def check_data_params(self, out_log):
        """ Checks input/output paths correctness """

        # Check input(s)
        self.io_dict["in"]["input_top_path"] = check_input_path(self.io_dict["in"]["input_top_path"], "input_top_path", False, out_log, self.__class__.__name__)
        self.io_dict["in"]["input_crd_path"] = check_input_path(self.io_dict["in"]["input_crd_path"], "input_crd_path", False, out_log, self.__class__.__name__)
        self.io_dict["in"]["input_mdin_path"] = check_input_path(self.io_dict["in"]["input_mdin_path"], "input_mdin_path", True, out_log, self.__class__.__name__)

        # Check output(s) -- Not really sure is needed...
        #self.io_dict["out"]["output_log_path"] = check_output_path(self.io_dict["out"]["output_log_path"],"output_log_path", False, out_log, self.__class__.__name__)
        #self.io_dict["out"]["output_traj_path"] = check_output_path(self.io_dict["out"]["output_traj_path"],"output_traj_path", False, out_log, self.__class__.__name__)
        #self.io_dict["out"]["output_rst_path"] = check_output_path(self.io_dict["out"]["output_rst_path"],"output_rst_path", False, out_log, self.__class__.__name__)

    def create_mdin(self, path: str = None) -> str:
        """Creates an AMBER MD configuration file (mdin) using the properties file settings"""
        mdin_list = []

        self.output_mdin_path = path

        if self.io_dict['in']['input_mdin_path']:
            # MDIN parameters read from an input mdin file
            mdin_list.append("Mdin read from input file: " + self.io_dict['in']['input_mdin_path'])
            mdin_list.append("and modified by the biobb_amber module from the BioBB library ")
            mdin_list.append("&cntrl")
            with open(self.io_dict['in']['input_mdin_path']) as input_params:
                for line in input_params:
                    if '=' in line:
                        mdin_list.append(line.rstrip())
        else:
            # MDIN parameters added by the biobb_amber module
            mdin_list.append("This mdin file has been created by the biobb_amber module from the BioBB library ")

            sim_type = self.properties.get('simulation_type', 'minimization')
            #sim_type = self.mdin.get('simulation_type', 'minimization')
            minimization = (sim_type == 'minimization')
            min_vacuo = (sim_type == 'min_vacuo')
            heat = (sim_type == 'heat')
            nvt = (sim_type == 'nvt')
            npt = (sim_type == 'npt')
            free = (sim_type == 'free')
            md = (nvt or npt or free)

            mdin_list.append("Type of mdin: " + sim_type)
            mdin_list.append("&cntrl")

            # Pre-configured simulation type parameters
            if minimization:
                mdin_list.append("  imin = 1")
            if md:
                mdin_list.append("  imin = 0")
            if min_vacuo:
                mdin_list.append("  imin = 1")
                mdin_list.append("  ncyc = 250")
                mdin_list.append("  ntb = 0")
                mdin_list.append("  igb = 0")
                mdin_list.append("  cut = 12")
            if heat:
                mdin_list.append("  tempi = 0.0")
                mdin_list.append("  temp0 = 300.0")
                mdin_list.append("  irest = 0")
                mdin_list.append("  ntb = 1") #periodic boundaries
                mdin_list.append("  cut = 10.0")
                mdin_list.append("  ntr = 0")
                mdin_list.append("  ntc = 2")
                mdin_list.append("  ntf = 2")
                mdin_list.append("  ntt = 3")
                mdin_list.append("  ig = -1")
                mdin_list.append("  ioutfm = 1")
                mdin_list.append("  iwrap = 1")
                mdin_list.append("  gamma_ln = 1.0")
                mdin_list.append("  nstlim = 5000")
                mdin_list.append("  dt = 0.002")
            if npt:
                mdin_list.append("  irest = 1")
                mdin_list.append("  ntx = 5")
                mdin_list.append("  pres0 = 1.0")
                mdin_list.append("  ntp = 1")
                mdin_list.append("  taup = 2.0")
                mdin_list.append("  cut = 10.0")
                mdin_list.append("  ntr = 0")
                mdin_list.append("  ntc = 2")
                mdin_list.append("  ntf = 2")
                mdin_list.append("  ntt = 3")
                mdin_list.append("  gamma_ln = 5.0")
                mdin_list.append("  ig = -1")
                mdin_list.append("  ioutfm = 1")
                mdin_list.append("  iwrap = 1")
                mdin_list.append("  nstlim = 5000")
                mdin_list.append("  dt = 0.002")

        # Adding the rest of parameters in the config file to the mdin file
        # if the parameter has already been added replace the value
        parameter_keys = [parameter.split('=')[0].strip() for parameter in mdin_list]
        for k, v in self.mdin.items():
            config_parameter_key = str(k).strip()
            if config_parameter_key in parameter_keys:
                mdin_list[parameter_keys.index(config_parameter_key)] = '  ' + config_parameter_key + ' = '+str(v)
            else:
                mdin_list.append('  ' + config_parameter_key + ' = '+str(v))

        # End of file keyword
        mdin_list.append("&end")

        # Writing MD configuration file (mdin)
        with open(self.output_mdin_path, 'w') as mdin:
            for line in mdin_list:
                mdin.write(line + '\n')

        return self.output_mdin_path

    @launchlogger
    def launch(self):
        """Launches the execution of the BuildLinearStructure module."""

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        # check input/output paths and parameters
        self.check_data_params(out_log)

        # Check the properties
        fu.check_properties(self, self.properties)

        # Restart
        if self.restart:
            output_file_list = [self.io_dict['out']['output_traj_path'],
                                self.io_dict['out']['output_rst_path']]
            if fu.check_complete_files(output_file_list):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step, out_log, self.global_log)
                return 0

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir()
        fu.log('Creating %s temporary folder' % self.tmp_folder, out_log)

        #if self.io_dict['in']['input_mdin_path']:
        #    self.output_mdin_path = self.io_dict['in']['input_mdin_path']
        #else:
        #    self.output_mdin_path = self.create_mdin(path=str(Path(self.tmp_folder).joinpath("pmemd.mdin")))
        self.output_mdin_path = self.create_mdin(path=str(Path(self.tmp_folder).joinpath("pmemd.mdin")))

        # Command line
        # pmemd -O -i mdin/min.mdin -p $1.cpH.prmtop -c ph$i/$1.inpcrd -r ph$i/$1.min.rst7 -o ph$i/$1.min.o
        cmd = [self.pmemd_path,
               '-O',
               '-i', self.output_mdin_path,
               '-p', self.io_dict['in']['input_top_path'],
               '-c', self.io_dict['in']['input_crd_path'],
               '-r', self.io_dict['out']['output_rst_path'],
               '-o', self.io_dict['out']['output_log_path'],
               '-x', self.io_dict['out']['output_traj_path']
               ]

        if self.io_dict['in']['input_ref_path']:
            cmd.append('-ref ')
            cmd.append(self.io_dict['in']['input_ref_path'])

        # general mpi properties
        if self.mpi_bin:
            mpi_cmd = [self.mpi_bin]
            if self.mpi_np:
                mpi_cmd.append('-n')
                mpi_cmd.append(str(self.mpi_np))
            if self.mpi_hostlist:
                mpi_cmd.append('-hostfile')
                mpi_cmd.append(self.mpi_hostlist)
            cmd = mpi_cmd + cmd

        fu.log('Creating command line with instructions and required arguments', out_log, self.global_log)

        # Launch execution
        returncode = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()

        # Remove temporary file(s)
        if self.remove_tmp:
            fu.rm(self.tmp_folder)
            fu.rm("mdinfo")
            fu.log('Removed: mdinfo, %s' % str(self.tmp_folder), out_log)

        return returncode

def pmemd_mdrun(input_top_path: str, input_crd_path: str,
            output_log_path: str, output_traj_path: str, output_rst_path: str,
            input_mdin_path: str = None, input_cpin_path: str = None,
            output_cpout_path: str = None, output_cprst_path: str = None,
            output_mdinfo_path: str = None, input_ref_path: str=None,
            properties: dict = None, **kwargs) -> int:
    """Create :class:`PmemdMDRun <pmemd.pmemd_mdrun.PmemdMDRun>`pmemd.pmemd_mdrun.PmemdMDRun class and
    execute :meth:`launch() <pmemd.pmemd_mdrun.PmemdMDRun.launch>` method"""

    return PmemdMDRun( input_top_path=input_top_path,
                    input_crd_path=input_crd_path,
                    input_mdin_path=input_mdin_path,
                    input_cpin_path=input_cpin_path,
                    input_ref_path=input_ref_path,
                    output_log_path=output_log_path,
                    output_traj_path=output_traj_path,
                    output_rst_path=output_rst_path,
                    output_cpout_path=output_cpout_path,
                    output_cprst_path=output_cprst_path,
                    output_mdinfo_path=output_mdinfo_path,
                    properties=properties).launch()

def main():
    parser = argparse.ArgumentParser(description='Running molecular dynamics using pmemd tool from the AMBER MD package.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_top_path', required=True, help='Input topology file (AMBER ParmTop). Accepted formats: top, prmtop, parmtop.')
    required_args.add_argument('--input_crd_path', required=True, help='Input coordinates file (AMBER crd). Accepted formats: crd, mdcrd.')
    required_args.add_argument('--input_mdin_path', required=False, help='Input configuration file (MD run options) (AMBER mdin). Accepted formats: mdin, in, txt.')
    required_args.add_argument('--input_cpin_path', required=False, help='Input constant pH file (AMBER cpin). Accepted formats: cpin.')
    required_args.add_argument('--input_ref_path', required=False, help='Input reference coordinates for position restraints. Accepted formats: rst, rst7.')
    required_args.add_argument('--output_log_path', required=True, help='Output log file. Accepted formats: log, out, txt.')
    required_args.add_argument('--output_traj_path', required=True, help='Output trajectory file. Accepted formats: trj, crd, mdcrd, x.')
    required_args.add_argument('--output_rst_path', required=True, help='Output restart file. Accepted formats: rst, rst7.')
    required_args.add_argument('--output_cpout_path', required=False, help='Output constant pH file (AMBER cpout). Accepted formats: cpout.')
    required_args.add_argument('--output_cprst_path', required=False, help='Output constant pH restart file (AMBER rstout). Accepted formats: cprst.')
    required_args.add_argument('--output_mdinfo_path', required=False, help='Output MD info. Accepted formats: mdinfo.')

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call
    PmemdMDRun(    input_top_path=args.input_top_path,
                    input_crd_path=args.input_crd_path,
                    input_mdin_path=args.input_mdin_path,
                    input_cpin_path=args.input_cpin_path,
                    input_ref_path=args.input_ref_path,
                    output_log_path=args.output_log_path,
                    output_traj_path=args.output_traj_path,
                    output_rst_path=args.output_rst_path,
                    output_cpout_path=args.output_cpout_path,
                    output_cprst_path=args.output_cprst_path,
                    output_mdinfo_path=args.output_mdinfo_path,
                    properties=properties).launch()

if __name__ == '__main__':
    main()
