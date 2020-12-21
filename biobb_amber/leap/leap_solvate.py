#!/usr/bin/env python3

"""Module containing the LeapSolvate class and the command line interface."""
import argparse
import shutil, re
from pathlib import Path, PurePath
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_amber.leap.common import *

class LeapSolvate():
    """
    | biobb_amber LeapSolvate
    | Wrapper of the `AmberTools (AMBER MD Package) leap tool <https://ambermd.org/AmberTools.php>`_ module.
    | Creates and solvates a system box for an AMBER MD system using tLeap tool from the AmberTools MD package.

    Args:
        input_pdb_path (str): Input 3D structure PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/structure.pdb>`_. Accepted formats: pdb (edam:format_1476).
        input_lib_path (str) (Optional): Input ligand library parameters file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/ligand.lib>`_. Accepted formats: lib (edam:format_3889).
        input_frcmod_path (str) (Optional): Input ligand frcmod parameters file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/ligand.frcmod>`_. Accepted formats: frcmod (edam:format_3888).
        output_pdb_path (str): Output 3D structure PDB file matching the topology file. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/structure.solv.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_top_path (str): Output topology file (AMBER ParmTop). File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/structure.solv.top>`_. Accepted formats: top (edam:format_3881), parmtop (edam:format_3881), prmtop (edam:format_3881).
        output_crd_path (str): Output coordinates file (AMBER crd). File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/structure.solv.crd>`_. Accepted formats: crd (edam:format_3878), mdcrd (edam:format_3878), inpcrd (edam:format_3878).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **forcefield** (*str*) - ("protein.ff14SB") Forcefield to be used for the structure generation. Values: protein.ff14SB, protein.ff19SB, DNA.bsc1, DNA.OL15, RNA.OL3.
            * **water_type** (*str*) - ("TIP3PBOX") Water molecule parameters to be used for the topology. Values: POL3BOX, QSPCFWBOX, SPCBOX, SPCFWBOX, TIP3PBOX, TIP3PFBOX, TIP4PBOX, TIP4PEWBOX, OPCBOX, OPC3BOX, TIP5PBOX.
            * **box_type** (*str*) - ("truncated_octahedron") Type for the MD system box. Values: cubic, truncated_octahedron.
            * **neutralise** (*bool*) - ("True") Energetically neutralise the system adding the necessary counterions.
            * **positive_ions_number** (*int*) - (0) Number of additional positive ions to include in the system box.
            * **negative_ions_number** (*int*) - (0) Number of additional negative ions to include in the system box.
            * **positive_ions_type** (*str*) - ("Na+") Type of additional positive ions to include in the system box. Values: Na+,K+.
            * **negative_ions_type** (*str*) - ("Cl-") Type of additional negative ions to include in the system box. Values: Cl-.
            * **distance_to_molecule** (*float*) - ("8.0") Size for the MD system box, defined such as the minimum distance between any atom originally present in solute and the edge of the periodic box is given by this distance parameter.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::
            from biobb_amber.leap.leap_solvate import leap_solvate
            prop = {
                'forcefield': 'protein.ff14SB',
                'water_type': 'TIP3PBOX',
                'box_type': 'truncated_octahedron',
                'neutralise' : True
            }
            leap_solvate(input_pdb_path='/path/to/structure.pdb',
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
    properties: dict = None, **kwargs):
        properties = properties or {}

        # Input/Output files
        self.io_dict = {
            'in': { 'input_pdb_path': input_pdb_path,
                    'input_lib_path': input_lib_path,
                    'input_frcmod_path': input_frcmod_path
            },
            'out': {    'output_pdb_path': output_pdb_path,
                        'output_top_path': output_top_path,
                        'output_crd_path': output_crd_path }
        }

        # Ligand Parameter lists
        self.ligands_lib_list = []
        if input_lib_path:
            self.ligands_lib_list.append(input_lib_path)

        self.ligands_frcmod_list = []
        if input_frcmod_path:
            self.ligands_frcmod_list.append(input_frcmod_path)

        # Properties specific for BB
        self.properties = properties
        self.forcefield = properties.get('forcefield', "protein.ff14SB")
        self.water_type = properties.get('water_type', "TIP3PBOX")
        self.box_type = properties.get('box_type', "truncated_octahedron")
        self.neutralise = properties.get('neutralise', True)
        self.positive_ions_number = properties.get('positive_ions_number', 0)
        self.positive_ions_type = properties.get('positive_ions_type', "Na+")
        self.negative_ions_number = properties.get('negative_ions_number', 0)
        self.negative_ions_type = properties.get('negative_ions_type', "Cl-")
        self.distance_to_molecule = properties.get('distance_to_molecule', 8.0)

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
        """Launches the execution of the LeapSolvate module."""

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

        # create .in file
        # source leaprc.constph
        # source leaprc.water.tip3p
        # foo = sequence { ACE TYR TYR AS4 PRO GL4 THR GLY THR TRP TYR NME }
        # solvateoct foo TIP3PBOX 12 iso
        # addions foo Cl- 0
        # addions foo Na+ 0
        # saveamberparm foo xxxx.prmtop xxxx.inpcrd
        # savepdb foo xxxx.pdb
        # quit

        box_command = "solvateOct"
        if self.box_type == "cubic":
            box_command = "solvateBox"

        # Forcefield
        source_ff_command = "source leaprc." + self.forcefield

        # Water Type
        # leaprc.water.tip4pew, tip4pd, tip3p, spceb, spce, opc, fb4, fb3
        # Values: POL3BOX, QSPCFWBOX, SPCBOX, SPCFWBOX, TIP3PBOX, TIP3PFBOX, TIP4PBOX, TIP4PEWBOX, OPCBOX, OPC3BOX, TIP5PBOX.
        source_wat_command = "source leaprc.water.tip3p"
        if self.water_type == "TIP4PEWBOX":
            source_wat_command = "leaprc.water.tip4pew"
        if self.water_type == "TIP4PBOX":
            source_wat_command = "leaprc.water.tip4pd"
        if re.match(r"SPC", self.water_type):
            source_wat_command = "source leaprc.water.spce"
        if re.match(r"OPC", self.water_type):
            source_wat_command = "source leaprc.water.opc"

        # Counterions
        ions_command = ""
        if self.neutralise:
            ions_command = ions_command + "addions mol " + self.negative_ions_type + " 0 \n"
            ions_command = ions_command + "addions mol " + self.positive_ions_type + " 0 \n"

        if self.negative_ions_number != 0:
            ions_command = ions_command + "addions mol " + self.negative_ions_type + " " + str(self.negative_ions_number) + " \n"
        if self.positive_ions_number != 0:
            ions_command = ions_command + "addions mol " + self.positive_ions_type + " " + str(self.positive_ions_number) + " \n"

        instructions_file = str(PurePath(self.tmp_folder).joinpath("leap.in"))
        with open(instructions_file, 'w') as leapin:
                leapin.write("source leaprc.DNA.bsc1 \n")
                leapin.write("source leaprc.protein.ff14SB \n")
                leapin.write("source leaprc.gaff \n")
                leapin.write(source_ff_command + " \n")
                leapin.write(source_wat_command + " \n")
                for amber_lib in self.ligands_lib_list:
                    leapin.write("loadOff " + amber_lib + "\n")
                for amber_frcmod in self.ligands_frcmod_list:
                    leapin.write("loadamberparams " + amber_frcmod + "\n")
                leapin.write("mol = loadpdb " + self.io_dict['in']['input_pdb_path'] + " \n")
                leapin.write(box_command + " mol " + self.water_type + " " + str(self.distance_to_molecule) + " \n")
                leapin.write(ions_command)
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

def leap_solvate(input_pdb_path: str, output_pdb_path: str,
           output_top_path: str, output_crd_path: str,
           properties: dict = None) -> int:
    """Create :class:`LeapSolvate <leap.leap_solvate.LeapSolvate>`leap.leap_solvate.LeapSolvate class and
    execute :meth:`launch() <leap.leap_solvate.LeapSolvate.launch>` method"""

    return LeapSolvate( input_pdb_path=input_pdb_path,
                        output_pdb_path=output_pdb_path,
                        output_top_path=output_top_path,
                        output_crd_path=output_crd_path,
                        properties=properties).launch()

def main():
    parser = argparse.ArgumentParser(description='Generating and solvating a system box for an AMBER MD system. using tLeap program from AmberTools MD package.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_pdb_path', required=True, help='Input 3D structure PDB file. Accepted formats: pdb.')
    required_args.add_argument('--output_pdb_path', required=True, help='Output 3D structure PDB file matching the topology file. Accepted formats: pdb.')
    required_args.add_argument('--output_top_path', required=True, help='Output topology file (AMBER ParmTop). Accepted formats: top.')
    required_args.add_argument('--output_crd_path', required=True, help='Output coordinates file (AMBER crd). Accepted formats: crd.')

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call
    LeapSolvate(   input_pdb_path=args.input_pdb_path,
                            output_pdb_path=args.output_pdb_path,
                            output_top_path=args.output_top_path,
                            output_crd_path=args.output_crd_path,
                            properties=properties).launch()

if __name__ == '__main__':
    main()
