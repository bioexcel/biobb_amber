#!/usr/bin/env python3

"""Module containing the SanderMDRun class and the command line interface."""
import argparse
import shutil, re
from pathlib import Path, PurePath
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_amber.sander.common import *

class SanderMDRun():
    """
    | biobb_amber SanderMDRun
    | Wrapper of the `AmberTools (AMBER MD Package) sander tool <https://ambermd.org/AmberTools.php>`_ module.
    | Runs energy minimization, molecular dynamics, and NMR refinements using sander tool from the AmberTools MD package.

    Args:
        input_top_path (str): Input topology file (AMBER ParmTop). File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/sander/cln025.prmtop>`_. Accepted formats: top (edam:format_3881), parmtop (edam:format_3881), prmtop (edam:format_3881).
        input_crd_path (str): Input coordinates file (AMBER crd). File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/sander/cln025.inpcrd>`_. Accepted formats: crd (edam:format_3878), mdcrd (edam:format_3878), inpcrd (edam:format_3878), netcdf (edam:format_3650), nc (edam:format_3650), ncrst (edam:format_3650).
        input_mdin_path (str) (Optional): Input configuration file (MD run options) (AMBER mdin). File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/sander/npt.mdin>`_. Accepted formats: mdin (edam:format_2330), in (edam:format_2330), txt (edam:format_2330).
        input_cpin_path (str) (Optional): Input constant pH file (AMBER cpin). File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/sander/cln025.cpin>`_. Accepted formats: cpin (edam:format_2330).
        input_ref_path (str) (Optional): Input reference coordinates for position restraints. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/sander/sander.rst>`_. Accepted formats: rst (edam:format_3886), rst7 (edam:format_3886), netcdf (edam:format_3650), nc (edam:format_3650), ncrst (edam:format_3650).
        output_log_path (str): Output log file. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/sander/sander.log>`_. Accepted formats: log (edam:format_2330), out (edam:format_2330), txt (edam:format_2330), o (edam:format_2330).
        output_traj_path (str): Output trajectory file. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/sander/sander.x>`_. Accepted formats: trj (edam:format_3878), crd (edam:format_3878), mdcrd (edam:format_3878), x (edam:format_3878), netcdf (edam:format_3650), nc (edam:format_3650).
        output_rst_path (str): Output restart file. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/sander/sander.rst>`_. Accepted formats: rst (edam:format_3886), rst7 (edam:format_3886), netcdf (edam:format_3650), nc (edam:format_3650), ncrst (edam:format_3650).
        output_cpout_path (str) (Optional): Output constant pH file (AMBER cpout). File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/sander/sander.cpout>`_. Accepted formats: cpout (edam:format_2330).
        output_cprst_path (str) (Optional): Output constant pH restart file (AMBER rstout). File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/sander/sander.cprst>`_. Accepted formats: cprst (edam:format_3886), rst (edam:format_3886), rst7 (edam:format_3886).
        output_mdinfo_path (str) (Optional): Output MD info. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/sander/sander.mdinfo>`_. Accepted formats: mdinfo (edam:format_2330).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **mdin** (*dict*) - ({}) Sander MD run options specification. (Used if *input_mdin_path* is None)
            * **simulation_type** (*str*) - ("minimization") Default options for the mdin file. Each creates a different mdin file. Values: `minimization <https://biobb-amber.readthedocs.io/en/latest/_static/mdins/min.mdin>`_ (Runs an energy minimization), `min_vacuo <https://biobb-amber.readthedocs.io/en/latest/_static/mdins/min_vacuo.mdin>`_ (Runs an energy minimization in vacuo), `NVT <https://biobb-amber.readthedocs.io/en/latest/_static/mdins/nvt.mdin>`_ (Runs an NVT equilibration), `npt <https://biobb-amber.readthedocs.io/en/latest/_static/mdins/npt.mdin>`_ (Runs an NPT equilibration), `free <https://biobb-amber.readthedocs.io/en/latest/_static/mdins/free.mdin>`_ (Runs a MD simulation), `heat <https://biobb-amber.readthedocs.io/en/latest/_static/mdins/heat.mdin>`_ (Heats the MD system).
            * **sander_path** (*str*) - ("sander") sander binary path to be used.
            * **mpi_bin** (*str*) - (None) Path to the MPI runner. Usually "mpirun" or "srun".
            * **mpi_np** (*int*) - (0) [0~1000|1] Number of MPI processes. Usually an integer bigger than 1.
            * **mpi_flags** (*str*) - (None) Path to the MPI hostlist file.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_amber.sander.sander_mdrun import sander_mdrun
            prop = {
                'simulation_type' : 'minimization',
                'mdin' : {
                    'dt' : 0.002
                }
            }
            sander_mdrun(input_top_path='/path/to/topology.top',
                         input_crd_path='/path/to/coordinates.crd',
                         output_traj_path='/path/to/newTrajectory.crd',
                         output_rst_path='/path/to/newRestart.rst',
                         output_log_path='/path/to/newAmberlog.log',
                         properties=prop)

    Info:
        * wrapped_software:
            * name: AmberTools Sander
            * version: >20.9
            * license: LGPL 2.1
            * multinode: mpi
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
        self.sander_path = properties.get('sander_path', "sander")
        self.mdin = {k: str(v) for k, v in properties.get('mdin', dict()).items()}

        if 'restraintmask' in self.mdin and self.mdin['restraintmask'][0] != '"' and self.mdin['restraintmask'][-1] != '"':
            self.mdin['restraintmask'] = "\"" + self.mdin['restraintmask'] + "\""
            
        # Properties for MPI
        self.mpi_bin = properties.get('mpi_bin')
        self.mpi_np = properties.get('mpi_np')
        self.mpi_flags = properties.get('mpi_flags')

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
        self.io_dict["in"]["input_cpin_path"] = check_input_path(self.io_dict["in"]["input_cpin_path"], "input_cpin_path", True, out_log, self.__class__.__name__)
        self.io_dict["in"]["input_ref_path"] = check_input_path(self.io_dict["in"]["input_ref_path"], "input_ref_path", True, out_log, self.__class__.__name__)

        # Check output(s)
        self.io_dict["out"]["output_log_path"] = check_output_path(self.io_dict["out"]["output_log_path"],"output_log_path", False, out_log, self.__class__.__name__)
        self.io_dict["out"]["output_traj_path"] = check_output_path(self.io_dict["out"]["output_traj_path"],"output_traj_path", False, out_log, self.__class__.__name__)
        self.io_dict["out"]["output_rst_path"] = check_output_path(self.io_dict["out"]["output_rst_path"],"output_rst_path", False, out_log, self.__class__.__name__)
        self.io_dict["out"]["output_cpout_path"] = check_output_path(self.io_dict["out"]["output_cpout_path"],"output_cpout_path", True, out_log, self.__class__.__name__)
        self.io_dict["out"]["output_cprst_path"] = check_output_path(self.io_dict["out"]["output_cprst_path"],"output_cprst_path", True, out_log, self.__class__.__name__)
        self.io_dict["out"]["output_mdinfo_path"] = check_output_path(self.io_dict["out"]["output_mdinfo_path"],"output_mdinfo_path", True, out_log, self.__class__.__name__)

    def create_mdin(self, path: str = None) -> str:
        """Creates an AMBER MD configuration file (mdin) using the properties file settings"""
        mdin_list = []
        mdin_firstPart = []
        mdin_middlePart = []
        mdin_lastPart = []

        self.output_mdin_path = path

        if self.io_dict['in']['input_mdin_path']:
            # MDIN parameters read from an input mdin file
            mdin_firstPart.append("Mdin read from input file: " + self.io_dict['in']['input_mdin_path'])
            mdin_firstPart.append("and modified by the biobb_amber module from the BioBB library ")
            with open(self.io_dict['in']['input_mdin_path']) as input_params:
                firstPart = True
                secondPart = False
                for line in input_params:
                    if '=' in line and not secondPart:
                        firstPart = False
                        mdin_middlePart.append(line.rstrip())
                    else:
                        if (firstPart):
                            mdin_firstPart.append(line.rstrip())
                        elif(secondPart):
                            mdin_lastPart.append(line.rstrip())
                        else:
                            secondPart = True
                            mdin_lastPart.append(line.rstrip())

            for line in mdin_middlePart:
                if ('!' in line or '#' in line) and not ('!@' in line or '!:' in line):
                    # Parsing lines with comments (#,!), e.g. :
                    # ntc=2, ntf=2, ! SHAKE, constrain lenghts of the bonds having H
                    params = re.split('!|#',line)
                    for param in params[0].split(','):
                        if param.strip():
                            mdin_list.append("  " + param.strip() + " ! " + params[1])
                elif ('@' in line or ':' in line):
                    # Parsing masks, e.g. :
                    # restraintmask = ":1-40@P,O5',C5',C4',C3',O3'", restraint_wt = 0.5
                    mylist = re.findall(r'(?:[^,"]|"(?:\\.|[^"])*")+', line)
                    [mdin_list.append("  " + i.lstrip()) for i in mylist]
                else:
                    for param in line.split(','):
                        if param.strip():
                            if not param.strip().startswith('!'):
                                mdin_list.append("  " + param.strip())

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
            md = (nvt or npt or free or heat)

            mdin_list.append("Type of mdin: " + sim_type)
            mdin_list.append("&cntrl")

            # Pre-configured simulation type parameters
            if minimization:
                mdin_list.append("  imin = 1 ! BioBB simulation_type minimization")
            if min_vacuo:
                mdin_list.append("  imin = 1 ! BioBB simulation_type min_vacuo")
                mdin_list.append("  ncyc = 250 ! BioBB simulation_type min_vacuo")
                mdin_list.append("  ntb = 0 ! BioBB simulation_type min_vacuo")
                mdin_list.append("  igb = 0 ! BioBB simulation_type min_vacuo")
                mdin_list.append("  cut = 12 ! BioBB simulation_type min_vacuo")
            if md:
                mdin_list.append("  imin = 0 ! BioBB simulation_type nvt|npt|free|heat")
                mdin_list.append("  cut = 10.0 ! BioBB simulation_type nvt|npt|free|heat")
                mdin_list.append("  ntr = 0 ! BioBB simulation_type nvt|npt|free|heat")
                mdin_list.append("  ntc = 2 ! BioBB simulation_type nvt|npt|free|heat")
                mdin_list.append("  ntf = 2 ! BioBB simulation_type nvt|npt|free|heat")
                mdin_list.append("  ntt = 3 ! BioBB simulation_type nvt|npt|free|heat")
                mdin_list.append("  ig = -1 ! BioBB simulation_type nvt|npt|free|heat")
                mdin_list.append("  ioutfm = 1 ! BioBB simulation_type nvt|npt|free|heat")
                mdin_list.append("  iwrap = 1 ! BioBB simulation_type nvt|npt|free|heat")
                mdin_list.append("  nstlim = 5000 ! BioBB simulation_type nvt|npt|free|heat")
                mdin_list.append("  dt = 0.002 ! BioBB simulation_type nvt|npt|free|heat")
            if npt:
                mdin_list.append("  irest = 1 ! BioBB simulation_type npt")
                mdin_list.append("  gamma_ln = 5.0 ! BioBB simulation_type npt")
                mdin_list.append("  pres0 = 1.0 ! BioBB simulation_type npt")
                mdin_list.append("  ntp = 1 ! BioBB simulation_type npt")
                mdin_list.append("  taup = 2.0 ! BioBB simulation_type npt")
                mdin_list.append("  ntx = 5 ! BioBB simulation_type npt")
            if nvt:
                mdin_list.append("  irest = 1 ! BioBB simulation_type nvt")
                mdin_list.append("  gamma_ln = 5.0 ! BioBB simulation_type nvt")
                mdin_list.append("  ntb = 1 ! BioBB simulation_type nvt")
                mdin_list.append("  ntx = 5 ! BioBB simulation_type nvt")
            if heat:
                mdin_list.append("  tempi = 0.0 ! BioBB simulation_type heat")
                mdin_list.append("  temp0 = 300.0 ! BioBB simulation_type heat")
                mdin_list.append("  irest = 0 ! BioBB simulation_type heat")
                mdin_list.append("  ntb = 1 ! BioBB simulation_type heat") #periodic boundaries
                mdin_list.append("  gamma_ln = 1.0 ! BioBB simulation_type heat")
                #mdin_list.append("  nmropt = 1 ! BioBB simulation_type heat")

                #mdin_lastPart.append("/")
                #mdin_lastPart.append("&wt")
                #mdin_lastPart.append(" TYPE = 'TEMP0' ! BioBB simulation_type heat")
                #mdin_lastPart.append(" ISTEP1 = 1 ! BioBB simulation_type heat")
                #mdin_lastPart.append(" ISTEP2 = 4000 ! BioBB simulation_type heat")
                #mdin_lastPart.append(" VALUE1 = 10.0 ! BioBB simulation_type heat")
                #mdin_lastPart.append(" VALUE2 = 300.0 ! BioBB simulation_type heat")
                #mdin_lastPart.append("/")
                #mdin_lastPart.append("&wt")
                #mdin_lastPart.append(" TYPE = 'END' ! BioBB simulation_type heat")
                #mdin_lastPart.append("/")

        # Adding the rest of parameters in the config file to the mdin file
        # if the parameter has already been added replace the value
        parameter_keys = [parameter.split('=')[0].strip() for parameter in mdin_list]
        for k, v in self.mdin.items():
            config_parameter_key = str(k).strip()
            if config_parameter_key in parameter_keys:
                mdin_list[parameter_keys.index(config_parameter_key)] = '  ' + config_parameter_key + ' = ' + str(v) + ' ! BioBB property'
            else:
                mdin_list.append('  ' + config_parameter_key + ' = '+str(v) + ' ! BioBB property')

        # Writing MD configuration file (mdin)
        with open(self.output_mdin_path, 'w') as mdin:
            # Start of file keyword(s)
            if mdin_firstPart:
                for line in mdin_firstPart:
                    mdin.write(line + '\n')

            # MD config parameters
            for line in mdin_list:
                mdin.write(line + '\n')

            # End of file keyword(s)
            if mdin_lastPart:
                for line in mdin_lastPart:
                    mdin.write(line + '\n')
            else:
                mdin.write("&end\n")

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
        #    self.output_mdin_path = self.create_mdin(path=str(Path(self.tmp_folder).joinpath("sander.mdin")))
        self.output_mdin_path = self.create_mdin(path=str(Path(self.tmp_folder).joinpath("sander.mdin")))

        # Command line
        # sander -O -i mdin/min.mdin -p $1.cpH.prmtop -c ph$i/$1.inpcrd -r ph$i/$1.min.rst7 -o ph$i/$1.min.o
        cmd = [self.sander_path,
               '-O',
               '-i', self.output_mdin_path,
               '-p', self.io_dict['in']['input_top_path'],
               '-c', self.io_dict['in']['input_crd_path'],
               '-r', self.io_dict['out']['output_rst_path'],
               '-o', self.io_dict['out']['output_log_path'],
               '-x', self.io_dict['out']['output_traj_path']
               ]

        if self.io_dict['in']['input_ref_path']:
            cmd.append('-ref')
            cmd.append(self.io_dict['in']['input_ref_path'])

        if self.io_dict['in']['input_cpin_path']:
            cmd.append('-cpin')
            cmd.append(self.io_dict['in']['input_cpin_path'])

        if self.io_dict['out']['output_mdinfo_path']:
            cmd.append('-inf')
            cmd.append(self.io_dict['out']['output_mdinfo_path'])

        if self.io_dict['out']['output_cpout_path']:
            cmd.append('-cpout')
            cmd.append(self.io_dict['out']['output_cpout_path'])

        if self.io_dict['out']['output_cprst_path']:
            cmd.append('-cprestrt')
            cmd.append(self.io_dict['out']['output_cprst_path'])

        # general mpi properties
        if self.mpi_bin:
            mpi_cmd = [self.mpi_bin]
            if self.mpi_np:
                mpi_cmd.append('-n')
                mpi_cmd.append(str(self.mpi_np))
            if self.mpi_flags:
                mpi_cmd.extend(self.mpi_flags)
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

def sander_mdrun(input_top_path: str, input_crd_path: str,
            output_log_path: str, output_traj_path: str, output_rst_path: str,
            input_mdin_path: str = None, input_cpin_path: str = None,
            output_cpout_path: str = None, output_cprst_path: str = None,
            output_mdinfo_path: str = None, input_ref_path: str=None,
            properties: dict = None, **kwargs) -> int:
    """Create :class:`SanderMDRun <sander.sander_mdrun.SanderMDRun>`sander.sander_mdrun.SanderMDRun class and
    execute :meth:`launch() <sander.sander_mdrun.SanderMDRun.launch>` method"""

    return SanderMDRun( input_top_path=input_top_path,
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
    parser = argparse.ArgumentParser(description='Running energy minimization, molecular dynamics, and NMR refinements using sander tool from the AmberTools MD package.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_top_path', required=True, help='Input topology file (AMBER ParmTop). Accepted formats: top, prmtop, parmtop.')
    required_args.add_argument('--input_crd_path', required=True, help='Input coordinates file (AMBER crd). Accepted formats: crd, mdcrd.')
    #required_args.add_argument('--input_mdin_path', required=False, help='Input configuration file (MD run options) (AMBER mdin). Accepted formats: mdin, in, txt.')
    parser.add_argument('--input_mdin_path', required=False, help='Input configuration file (MD run options) (AMBER mdin). Accepted formats: mdin, in, txt.')
    #required_args.add_argument('--input_cpin_path', required=False, help='Input constant pH file (AMBER cpin). Accepted formats: cpin.')
    parser.add_argument('--input_cpin_path', required=False, help='Input constant pH file (AMBER cpin). Accepted formats: cpin.')
    #required_args.add_argument('--input_ref_path', required=False, help='Input reference coordinates for position restraints. Accepted formats: rst, rst7.')
    parser.add_argument('--input_ref_path', required=False, help='Input reference coordinates for position restraints. Accepted formats: rst, rst7.')
    required_args.add_argument('--output_log_path', required=True, help='Output log file. Accepted formats: log, out, txt.')
    required_args.add_argument('--output_traj_path', required=True, help='Output trajectory file. Accepted formats: trj, crd, mdcrd, x.')
    required_args.add_argument('--output_rst_path', required=True, help='Output restart file. Accepted formats: rst, rst7.')
    #required_args.add_argument('--output_cpout_path', required=False, help='Output constant pH file (AMBER cpout). Accepted formats: cpout.')
    parser.add_argument('--output_cpout_path', required=False, help='Output constant pH file (AMBER cpout). Accepted formats: cpout.')
    #required_args.add_argument('--output_cprst_path', required=False, help='Output constant pH restart file (AMBER rstout). Accepted formats: cprst.')
    parser.add_argument('--output_cprst_path', required=False, help='Output constant pH restart file (AMBER rstout). Accepted formats: cprst.')
    #required_args.add_argument('--output_mdinfo_path', required=False, help='Output MD info. Accepted formats: mdinfo.')
    parser.add_argument('--output_mdinfo_path', required=False, help='Output MD info. Accepted formats: mdinfo.')

    args = parser.parse_args()
    #config = args.config if args.config else None
    args.config = args.config or "{}"
    #properties = settings.ConfReader(config=config).get_prop_dic()
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # Specific call
    sander_mdrun(    input_top_path=args.input_top_path,
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
                    properties=properties)

if __name__ == '__main__':
    main()
