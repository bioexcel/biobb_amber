#!/usr/bin/env python3

"""Module containing the LeapGenTop class and the command line interface."""
import argparse
import shutil
from pathlib import Path, PurePath
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_amber.leap.common import *

class LeapGenTop():
    """
    | biobb_amber.leap.leap_gen_top LeapGenTop
    | Wrapper of the `AmberTools (AMBER MD Package) leap tool <https://ambermd.org/AmberTools.php>`_ module.
    | Generates a MD topology from a molecule structure using tLeap tool from the AmberTools MD package.

    Args:
        input_pdb_path (str): Input 3D structure PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/structure.pdb>`_. Accepted formats: pdb (edam:format_1476).
        input_lib_path (str) (Optional): Input ligand library parameters file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/ligand.lib>`_. Accepted formats: lib (edam:format_3889).
        input_frcmod_path (str) (Optional): Input ligand frcmod parameters file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/ligand.frcmod>`_. Accepted formats: frcmod (edam:format_3888).
        input_params_path (str) (Optional): Additional leap parameter files to load with loadAmberParams Leap command. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/leapParams.in>`_. Accepted formats: in (edam:format_2330), leapin (edam:format_2330), txt (edam:format_2330), zip (edam:format_3987).
        input_source_path (str) (Optional): Additional leap command files to load with source Leap command. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/leapSource.in>`_. Accepted formats: in (edam:format_2330), leapin (edam:format_2330), txt (edam:format_2330), zip (edam:format_3987).
        output_pdb_path (str): Output 3D structure PDB file matching the topology file. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/structure.leap.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_top_path (str): Output topology file (AMBER ParmTop). File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/structure.leap.top>`_. Accepted formats: top (edam:format_3881), parmtop (edam:format_3881), prmtop (edam:format_3881).
        output_crd_path (str): Output coordinates file (AMBER crd). File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/structure.leap.crd>`_. Accepted formats: crd  (edam:format_3878), mdcrd (edam:format_3878), inpcrd (edam:format_3878).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **forcefield** (*list*) - (["protein.ff14SB","DNA.bsc1","gaff"]) Forcefield to be used for the structure generation. Values: protein.ff14SB, protein.ff19SB, DNA.bsc1, DNA.OL15, RNA.OL3, gaff.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_amber.leap.leap_gen_top import leap_gen_top
            prop = {
                'forcefield': ['protein.ff14SB']
            }
            leap_gen_top(input_pdb_path='/path/to/structure.pdb',
                          output_pdb_path='/path/to/newStructure.pdb',
                          output_top_path='/path/to/newTopology.top',
                          output_crd_path='/path/to/newCoordinates.crd',
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

    def __init__(self, input_pdb_path: str, output_pdb_path: str,
    output_top_path: str, output_crd_path: str,
    input_lib_path: str = None, input_frcmod_path: str = None,
    input_params_path: str = None, input_source_path: str = None,
    properties: dict = None, **kwargs):
        properties = properties or {}

        # Input/Output files
        self.io_dict = {
            'in': { 'input_pdb_path': input_pdb_path,
                    'input_lib_path': input_lib_path,
                    'input_frcmod_path': input_frcmod_path,
                    'input_params_path': input_params_path,
                    'input_source_path': input_source_path
             },
            'out': {    'output_pdb_path': output_pdb_path,
                        'output_top_path': output_top_path,
                        'output_crd_path': output_crd_path }
        }

        # # Ligand Parameter lists
        # self.ligands_lib_list = []
        # if input_lib_path:
        #     self.ligands_lib_list.append(input_lib_path)
        #
        # self.ligands_frcmod_list = []
        # if input_frcmod_path:
        #     self.ligands_frcmod_list.append(input_frcmod_path)

        # Properties specific for BB
        self.properties = properties
        self.forcefield = properties.get('forcefield', ["protein.ff14SB","DNA.bsc1","gaff"])

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
        self.io_dict["in"]["input_pdb_path"] = check_input_path(self.io_dict["in"]["input_pdb_path"], "input_pdb_path", out_log, self.__class__.__name__)

        # Check output(s) -- Not really sure is needed...
        #self.io_dict["out"]["output_pdb_path"] = check_output_path(self.io_dict["out"]["output_pdb_path"],"output_pdb_path", False, out_log, self.__class__.__name__)
        #self.io_dict["out"]["output_top_path"] = check_output_path(self.io_dict["out"]["output_top_path"],"output_top_path", False, out_log, self.__class__.__name__)
        #self.io_dict["out"]["output_crd_path"] = check_output_path(self.io_dict["out"]["output_crd_path"],"output_crd_path", False, out_log, self.__class__.__name__)

    @launchlogger
    def launch(self):
        """Launches the execution of the LeapGenTop module."""

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        # check input/output paths and parameters
        self.check_data_params(out_log)

        # Check the properties
        fu.check_properties(self, self.properties)

        # Restart
        if self.restart:
            output_file_list = [self.io_dict['out']['output_pdb_path'],
                                self.io_dict['out']['output_top_path'],
                                self.io_dict['out']['output_crd_path']]
            if fu.check_complete_files(output_file_list):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step, out_log, self.global_log)
                return 0

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir()
        fu.log('Creating %s temporary folder' % self.tmp_folder, out_log)

        # Leap configuration (instructions) file
        instructions_file = str(PurePath(self.tmp_folder).joinpath("leap.in"))

        ligands_lib_list = []
        if self.io_dict['in']['input_lib_path'] is not None:
            if self.io_dict['in']['input_lib_path'].endswith('.zip'):
                ligands_lib_list = fu.unzip_list(self.io_dict['in']['input_lib_path'], dest_dir=self.tmp_folder, out_log=out_log)
            else:
                ligands_lib_list.append(self.io_dict['in']['input_lib_path'])

        ligands_frcmod_list = []
        if self.io_dict['in']['input_frcmod_path'] is not None:
            if self.io_dict['in']['input_frcmod_path'].endswith('.zip'):
                ligands_frcmod_list = fu.unzip_list(self.io_dict['in']['input_frcmod_path'], dest_dir=self.tmp_folder, out_log=out_log)
            else:
                ligands_frcmod_list.append(self.io_dict['in']['input_frcmod_path'])

        amber_params_list = []
        if self.io_dict['in']['input_params_path'] is not None:
            if self.io_dict['in']['input_params_path'].endswith('.zip'):
                amber_params_list = fu.unzip_list(self.io_dict['in']['input_params_path'], dest_dir=self.tmp_folder, out_log=out_log)
            else:
                amber_params_list.append(self.io_dict['in']['input_params_path'])

        leap_source_list = []
        if self.io_dict['in']['input_source_path'] is not None:
            if self.io_dict['in']['input_source_path'].endswith('.zip'):
                leap_source_list = fu.unzip_list(self.io_dict['in']['input_source_path'], dest_dir=self.tmp_folder, out_log=out_log)
            else:
                leap_source_list.append(self.io_dict['in']['input_source_path'])

        with open(instructions_file, 'w') as leapin:
                # Forcefields loaded by default:
                # Protein: ff14SB (PARM99 + frcmod.ff99SB + frcmod.parmbsc0 + OL3 for RNA)
                #leapin.write("source leaprc.protein.ff14SB \n")
                # DNA: parmBSC1 (ParmBSC1 (ff99 + bsc0 + bsc1) for DNA. Ivani et al. Nature Methods 13: 55, 2016)
                #leapin.write("source leaprc.DNA.bsc1 \n")
                # Ligands: GAFF (General Amber Force field, J. Comput. Chem. 2004 Jul 15;25(9):1157-74)
                #leapin.write("source leaprc.gaff \n")

                # Forcefields loaded from input forcefield property
                for t in self.forcefield:
                    leapin.write("source leaprc.{}\n".format(t))

                # Additional Leap commands
                for leap_commands in leap_source_list:
                    leapin.write("source " + leap_commands + "\n")

                # Additional Amber parameters
                for amber_params in amber_params_list:
                    leapin.write("loadamberparams " + amber_params + "\n")

                # Ligand(s) libraries (if any)
                for amber_lib in ligands_lib_list:
                    leapin.write("loadOff " + amber_lib + "\n")
                for amber_frcmod in ligands_frcmod_list:
                    leapin.write("loadamberparams " + amber_frcmod + "\n")

                # Loading PDB file
                leapin.write("mol = loadpdb " + self.io_dict['in']['input_pdb_path'] + " \n")

                # Saving output PDB file, coordinates and topology
                leapin.write("savepdb mol " + self.io_dict['out']['output_pdb_path'] + " \n")
                leapin.write("saveAmberParm mol " + self.io_dict['out']['output_top_path'] + " " + self.io_dict['out']['output_crd_path'] + "\n")
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

def leap_gen_top(input_pdb_path: str, output_pdb_path: str,
           output_top_path: str, output_crd_path: str,
           input_lib_path: str = None, input_frcmod_path: str = None,
           input_params_path: str = None, input_source_path: str = None,
           properties: dict = None) -> int:
    """Create :class:`LeapGenTop <leap.leap_gen_top.LeapGenTop>`leap.leap_gen_top.LeapGenTop class and
    execute :meth:`launch() <leap.leap_gen_top.LeapGenTop.launch>` method"""

    return LeapGenTop( input_pdb_path=input_pdb_path,
                        input_lib_path=input_lib_path,
                        input_frcmod_path=input_frcmod_path,
                        input_params_path=input_params_path,
                        input_source_path=input_source_path,
                        output_pdb_path=output_pdb_path,
                        output_top_path=output_top_path,
                        output_crd_path=output_crd_path,
                        properties=properties).launch()

def main():
    parser = argparse.ArgumentParser(description='Generating a MD topology from a molecule structure using tLeap program from AmberTools MD package.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_pdb_path', required=True, help='Input 3D structure PDB file. Accepted formats: pdb.')
    required_args.add_argument('--input_lib_path', required=False, help='Input ligand library parameters file. Accepted formats: lib, zip.')
    required_args.add_argument('--input_frcmod_path', required=False, help='Input ligand frcmod parameters file. Accepted formats: frcmod, zip.')
    required_args.add_argument('--input_params_path', required=False, help='Additional leap parameter files to load with loadAmberParams Leap command. Accepted formats: leapin, in, txt, zip.')
    required_args.add_argument('--input_source_path', required=False, help='Additional leap command files to load with source Leap command. Accepted formats: leapin, in, txt, zip.')
    required_args.add_argument('--output_pdb_path', required=True, help='Output 3D structure PDB file matching the topology file. Accepted formats: pdb.')
    required_args.add_argument('--output_top_path', required=True, help='Output topology file (AMBER ParmTop). Accepted formats: top.')
    required_args.add_argument('--output_crd_path', required=True, help='Output coordinates file (AMBER crd). Accepted formats: crd.')

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call
    LeapGenTop(     input_pdb_path=args.input_pdb_path,
                    input_lib_path=args.input_lib_path,
                    input_frcmod_path=args.input_frcmod_path,
                    input_params_path=args.input_params_path,
                    input_source_path=args.input_source_path,
                    output_pdb_path=args.output_pdb_path,
                    output_top_path=args.output_top_path,
                    output_crd_path=args.output_crd_path,
                    properties=properties).launch()

if __name__ == '__main__':
    main()
