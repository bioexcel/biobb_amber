#!/usr/bin/env python3

"""Module containing the Pdb4amber class and the command line interface."""
import argparse
import shutil, re
from pathlib import Path, PurePath
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_amber.pdb4amber.common import *

class Pdb4amber():
    """
    | biobb_amber.pdb4amber.pdb4amber Pdb4amber
    | Wrapper of the `AmberTools (AMBER MD Package) pdb4amber tool <https://ambermd.org/AmberTools.php>`_ module.
    | Analyse PDB files and clean them for further usage, especially with the LEaP programs of Amber, using pdb4amber tool from the AmberTools MD package.

    Args:
        input_pdb_path (str): Input 3D structure PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pdb4amber/1aki_fixed.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_pdb_path (str): Output 3D structure PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/pdb4amber/structure.pdb4amber.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **remove_hydrogens** (*bool*) - (False) Remove hydrogen atoms from the PDB file.
            * **remove_waters** (*bool*) - (False) Remove water molecules from the PDB file.
            * **constant_pH** (*bool*) - (False) Rename ionizable residues e.g. GLU,ASP,HIS for constant pH simulation.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_amber.pdb4amber.pdb4amber import pdb4amber
            prop = {
                'remove_tmp': True
            }
            pdb4amber(input_pdb_path='/path/to/structure.pdb',
                          output_pdb_path='/path/to/newStructure.pdb',
                          properties=prop)

    Info:
        * wrapped_software:
            * name: AmberTools pdb4amber
            * version: >20.9
            * license: LGPL 2.1
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """
    def __init__(self, input_pdb_path: str, output_pdb_path: str,
                 properties: dict, **kwargs):
        properties = properties or {}

        # Input/Output files
        self.io_dict = {
            'in': { 'input_pdb_path': input_pdb_path },
            'out': { 'output_pdb_path': output_pdb_path }
        }

        # Properties specific for BB
        self.properties = properties
        self.remove_hydrogens = properties.get('remove_hydrogens', False)
        self.remove_waters = properties.get('remove_waters', False)
        self.constant_pH = properties.get('constant_pH', False)

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
        self.io_dict["in"]["input_pdb_path"] = check_input_path(self.io_dict["in"]["input_pdb_path"], "input_pdb_path", False, out_log, self.__class__.__name__)

        # Check output(s)
        self.io_dict["out"]["output_pdb_path"] = check_output_path(self.io_dict["out"]["output_pdb_path"],"output_pdb_path", False, out_log, self.__class__.__name__)

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

        # Command line
        # sander -O -i mdin/min.mdin -p $1.cpH.prmtop -c ph$i/$1.inpcrd -r ph$i/$1.min.rst7 -o ph$i/$1.min.o
        cmd = ['pdb4amber ',
               '-i', self.io_dict['in']['input_pdb_path'],
               '-o', self.io_dict['out']['output_pdb_path']
               ]

        if self.remove_hydrogens:
            cmd.append("-y ")
        if self.remove_waters:
            cmd.append("-d ")
        if self.constant_pH:
            cmd.append("--constantph ")

        fu.log('Creating command line with instructions and required arguments', out_log, self.global_log)

        # Launch execution
        returncode = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()

        # Remove temporary file(s)
        if self.remove_tmp:
            fu.rm(self.tmp_folder)
            fu.log('Removed: %s' % str(self.tmp_folder), out_log)

        return returncode

def pdb4amber(input_pdb_path: str, output_pdb_path: str,
           properties: dict = None, **kwargs) -> int:
    """Create :class:`Pdb4amber <pdb4amber.pdb4amber.Pdb4amber>`pdb4amber.pdb4amber.Pdb4amber class and
    execute :meth:`launch() <pdb4amber.pdb4amber.Pdb4amber.launch>` method"""

    return Pdb4amber( input_pdb_path=input_pdb_path,
                        output_pdb_path=output_pdb_path,
                        properties=properties).launch()

def main():
    parser = argparse.ArgumentParser(description='Analyse PDB files and clean them for further usage, especially with the LEaP programs of Amber, using pdb4amber tool from the AmberTools MD package.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_pdb_path', required=True, help='Input 3D structure PDB file. Accepted formats: pdb.')
    required_args.add_argument('--output_pdb_path', required=True, help='Output 3D structure PDB file. Accepted formats: pdb.')

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call
    Pdb4amber(    input_pdb_path=args.input_pdb_path,
                    output_pdb_path=args.output_pdb_path,
                    properties=properties).launch()

if __name__ == '__main__':
    main()
