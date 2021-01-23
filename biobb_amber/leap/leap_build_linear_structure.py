#!/usr/bin/env python3

"""Module containing the LeapBuildLinearStructure class and the command line interface."""
import argparse
import shutil
from pathlib import Path, PurePath
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_amber.leap.common import *

class LeapBuildLinearStructure():
    """
    | biobb_amber.leap.leap_build_linear_structure LeapBuildLinearStructure
    | Wrapper of the `AmberTools (AMBER MD Package) leap tool <https://ambermd.org/AmberTools.php>`_ module.
    | Builds a linear (unfolded) 3D structure from an AA sequence using tLeap tool from the AmberTools MD package.

    Args:
        output_pdb_path (str): Linear (unfolded) 3D structure PDB file. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **sequence** (*str*) - ("ALA GLY SER PRO ARG ALA PRO GLY") Aminoacid sequence to convert to a linear 3D structure. Aminoacids should be written in 3-letter code, with a blank space between them.
            * **forcefield** (*list*) - (["protein.ff14SB","DNA.bsc1","gaff"]) Forcefield to be used for the structure generation. Values: protein.ff14SB, protein.ff19SB, DNA.bsc1, DNA.OL15, RNA.OL3, gaff.
            * **build_library** (*bool*) - (False) Generate AMBER lib file for the structure.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_amber.leap.leap_build_linear_structure import leap_build_linear_structure
            prop = {
                'sequence' : 'ALA PRO SER ARG LYS ASP GLU GLY GLY ALA',
                'build_library': False,
                'forcefield': ['protein.ff14SB']
            }
            leap_build_linear_structure(output_pdb_path='/path/to/newStructure.pdb',
                          properties=prop)


    Info:
        * wrapped_software:
            * name: AmberTools tLeap
            * version: >20.9
            * license: LGPL 2.1
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, output_pdb_path, properties, **kwargs):
        properties = properties or {}

        # Input/Output files
        self.io_dict = {
            'out': { 'output_pdb_path': output_pdb_path }
        }

        # Properties specific for BB
        self.properties = properties
        self.sequence = properties.get('sequence', "ALA GLY SER PRO ARG ALA PRO GLY")
        self.forcefield = properties.get('forcefield', ["protein.ff14SB","DNA.bsc1","gaff"])
        self.build_library = properties.get('build_library', False)

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

        # Check output(s)
        self.io_dict["out"]["output_pdb_path"] = check_output_path(self.io_dict["out"]["output_pdb_path"],"output_pdb_path", False, out_log, self.__class__.__name__)

    @launchlogger
    def launch(self):
        """Launches the execution of the LeapBuildLinearStructure module."""

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        # check input/output paths and parameters
        self.check_data_params(out_log)

        # Check the properties
        fu.check_properties(self, self.properties)

        # Restart
        if self.restart:
            # 4. Include here all output file paths
            output_file_list = [self.io_dict['out']['output_pdb_path']]
            if fu.check_complete_files(output_file_list):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step, out_log, self.global_log)
                return 0

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir()
        fu.log('Creating %s temporary folder' % self.tmp_folder, out_log)

        # create .in file
        #TC5b = sequence { NASN LEU TYR ILE GLN TRP LEU LYS ASP GLY GLY PRO SER SER GLY ARG PRO PRO PRO CSER }
        #savepdb TC5b TC5b_linear.pdb
        #quit

        instructions_file = str(PurePath(self.tmp_folder).joinpath("leap.in"))
        with open(instructions_file, 'w') as leapin:

                # Forcefields loaded from input forcefield property
                for t in self.forcefield:
                    leapin.write("source leaprc.{}\n".format(t))

                leapin.write("struct = sequence {" + self.sequence + " } \n")
                leapin.write("savepdb struct " + self.io_dict['out']['output_pdb_path'] + "\n")
                leapin.write("quit \n");

        # Command line
        cmd = ['tleap ',
               '-f', instructions_file
               ]
        fu.log('Creating command line with instructions and required arguments', out_log, self.global_log)

        # Launch execution
        returncode = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()

        # Remove temporary file(s)
        if self.remove_tmp:
            fu.rm(self.tmp_folder)
            fu.rm("leap.log")
            fu.log('Removed: %s' % str(self.tmp_folder), out_log)
            fu.log('Removed: leap.log', out_log)

        return returncode

def leap_build_linear_structure(output_pdb_path: str,
           properties: dict = None, **kwargs) -> int:
    """Create :class:`LeapBuildLinearStructure <leap.leap_build_linear_structure.LeapBuildLinearStructure>`leap.leap_build_linear_structure.LeapBuildLinearStructure class and
    execute :meth:`launch() <leap.leap_build_linear_structure.LeapBuildLinearStructure.launch>` method"""

    return LeapBuildLinearStructure(
                        output_pdb_path=output_pdb_path,
                        properties=properties).launch()

def main():
    parser = argparse.ArgumentParser(description='Building a linear (unfolded) 3D structure from an AA sequence.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--output_pdb_path', required=True, help='Linear (unfolded) 3D structure PDB file. Accepted formats: pdb.')

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call
    LeapBuildLinearStructure(output_pdb_path=args.output_pdb_path,
             properties=properties).launch()

if __name__ == '__main__':
    main()
