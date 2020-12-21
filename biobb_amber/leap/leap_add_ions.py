#!/usr/bin/env python3

"""Module containing the LeapAddIons class and the command line interface."""
import argparse
import shutil, re
import subprocess
from decimal import Decimal
from pathlib import Path, PurePath
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_amber.leap.common import *

class LeapAddIons():
    """
    | biobb_amber LeapAddIons
    | Wrapper of the `AmberTools (AMBER MD Package) leap tool <https://ambermd.org/AmberTools.php>`_ module.
    | Adds counterions to a system box for an AMBER MD system using tLeap tool from the AmberTools MD package.

    Args:
        input_pdb_path (str): Input 3D structure PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/structure.pdb>`_. Accepted formats: pdb (edam:format_1476).
        input_lib_path (str) (Optional): Input ligand library parameters file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/ligand.lib>`_. Accepted formats: lib (edam:format_3889).
        input_frcmod_path (str) (Optional): Input ligand frcmod parameters file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/ligand.frcmod>`_. Accepted formats: frcmod (edam:format_3888).
        output_pdb_path (str): Output 3D structure PDB file matching the topology file. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/structure.ions.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_top_path (str): Output topology file (AMBER ParmTop). File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/structure.ions.top>`_. Accepted formats: top (edam:format_3881), parmtop (edam:format_3881), prmtop (edam:format_3881).
        output_crd_path (str): Output coordinates file (AMBER crd). File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/structure.ions.crd>`_. Accepted formats: crd  (edam:format_3878), mdcrd (edam:format_3878), inpcrd (edam:format_3878).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **forcefield** (*str*) - ("protein.ff14SB") Forcefield to be used for the structure generation. Values: protein.ff14SB, protein.ff19SB, DNA.bsc1, DNA.OL15, RNA.OL3.
            * **water_type** (*str*) - ("TIP3PBOX") Water molecule parameters to be used for the topology. Values: POL3BOX, QSPCFWBOX, SPCBOX, SPCFWBOX, TIP3PBOX, TIP3PFBOX, TIP4PBOX, TIP4PEWBOX, OPCBOX, OPC3BOX, TIP5PBOX.
            * **box_type** (*str*) - ("truncated_octahedron") Type for the MD system box. Values: cubic, truncated_octahedron.
            * **neutralise** (*bool*) - ("True") Energetically neutralise the system adding the necessary counterions.
            * **ionic_concentration** (*float*) - (0.05) Additional ionic concentration to include in the system box. Units in Mol/L.
            * **positive_ions_number** (*int*) - (0) Number of additional positive ions to include in the system box.
            * **negative_ions_number** (*int*) - (0) Number of additional negative ions to include in the system box.
            * **positive_ions_type** (*str*) - ("Na+") Type of additional positive ions to include in the system box. Values: Na+,K+.
            * **negative_ions_type** (*str*) - ("Cl-") Type of additional negative ions to include in the system box. Values: Cl-.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_amber.leap.leap_add_ions import leap_add_ions
            prop = {
                'forcefield': 'protein.ff14SB',
                'water_type': 'TIP3PBOX',
                'neutralise' : True
            }
            leap_add_ions(input_pdb_path='/path/to/structure.pdb',
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

    def __init__(self, input_pdb_path: str,
        output_pdb_path: str, output_top_path: str, output_crd_path: str,
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
        self.ionic_concentration = properties.get('ionic_concentration', 0.05)
        self.positive_ions_number = properties.get('positive_ions_number', 0)
        self.positive_ions_type = properties.get('positive_ions_type', "Na+")
        self.negative_ions_number = properties.get('negative_ions_number', 0)
        self.negative_ions_type = properties.get('negative_ions_type', "Cl-")

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

    def find_out_number_of_ions(self):
        """ Computes the number of positive and negative ions from the input ionic
        concentration and the number of water molecules in the system box."""

        # Finding number of water molecules in the box
        cnt = 0
        with open(self.io_dict['in']['input_pdb_path']) as fp:
           for line in fp:
               # Water molecules are identified with different resids
               # by different forcefields / MD packages
               pq = re.compile((r'WAT|HOH|TP3|TIP3|SOL'), re.M)
               if pq.search(line):
                   # Incrementing number of water molecules just in the water
                   # oxygen atom, ignoring hydrogen atoms
                   pq2 = re.compile(r"H", re.M)
                   if not pq2.search(line):
                       cnt = cnt + 1

        # To get to X mM ions we need
        # n(NaCl) = #waters / 55 Mol * X M
        # where X M = X mM / 1000
        self.nio = (cnt / 55) * (self.ionic_concentration / 1000)

    def tail(self, file, n_lines):
        """ Wrapper of the tail command line to extract the last
        n lines from a file."""
        proc = subprocess.Popen(['tail', '-n', n_lines, file], stdout=subprocess.PIPE)
        lines = proc.stdout.readlines()
        return lines

    def sed(self, file, out_file):
        """ Wrapper of the sed command line to remove the last
        line from a file."""
        proc = subprocess.Popen(['sed', '\'$d\'', file, ' > ', out_file], shell=True, stdout=subprocess.PIPE)
        lines = proc.stdout.readlines()

        return lines

    @launchlogger
    def launch(self):
        """Launches the execution of the LeapAddIons module."""

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

        # Forcefield
        source_ff_command = "source leaprc." + self.forcefield

        # Box type
        #box_command = "solvateOct"
        #if self.box_type == "cubic":
        #    box_command = "solvateBox"

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

        if self.ionic_concentration and self.negative_ions_number==0 and self.positive_ions_number==0:
            self.find_out_number_of_ions()
            nneg = self.nio # Update with function
            npos = self.nio # Update with function
            ions_command = ions_command + "addions mol " + self.negative_ions_type + " " + str(nneg) + " \n"
            ions_command = ions_command + "addions mol " + self.positive_ions_type + " " + str(npos) + " \n"
        else:
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
                #leapin.write(box_command + " mol " + self.water_type + " 0 \n")
                leapin.write(ions_command)
                leapin.write("setBox mol vdw \n")
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

        if self.box_type != "cubic":
            fu.log('Fixing truncated octahedron Box in the topology and restart files', out_log, self.global_log)

            # Taking box info from input PDB file, CRYST1 tag (first line)
            with open(self.io_dict['in']['input_pdb_path']) as file:
                lines = file.readlines()
                pdb_line = lines[0]

            if 'CRYST1' not in pdb_line:
                fu.log('WARNING: box info not found in input PDB file (CRYST1). Needed to correctly assign the octahedron box. Assuming cubic box.',out_log, self.global_log)
            else:
                # PDB info: CRYST1   86.316   86.316   86.316 109.47 109.47 109.47 P 1
                regex_box = 'CRYST1\s*(\d+\.\d+)\s*(\d+\.\d+)\s*(\d+\.\d+)\s*(\d+\.\d+)\s*(\d+\.\d+)\s*(\d+\.\d+)\s*P 1'
                box = re.findall(regex_box, pdb_line)[0]
                box_line = ""
                for coord in box:
                    box_line += "{:12.7f}".format(float(coord))

                # PRMTOP info: 1.09471219E+02  8.63157502E+01  8.63157502E+01  8.63157502E+01
                top_box_line = ""
                top_box_line += '  %.8E' % Decimal(float(box[3]))
                top_box_line += '  %.8E' % Decimal(float(box[0]))
                top_box_line += '  %.8E' % Decimal(float(box[1]))
                top_box_line += '  %.8E' % Decimal(float(box[2]))

                # Removing box generated by tleap from the crd file (last line)
                with open(self.io_dict['out']['output_crd_path']) as file:
                    lines = file.readlines()
                    crd_lines = lines[:-1]

                # Adding old box coordinates (taken from the input pdb)
                crd_lines.append(box_line)

                with open(self.io_dict['out']['output_crd_path'],'w') as file:
                    for line in crd_lines:
                        file.write(str(line))
                    file.write("\n")

                # Now fixing IFBOX param in prmtop.
                box_flag = False
                #%FLAG BOX_DIMENSIONS
                #%FORMAT(5E16.8)
                #1.09471219E+02  8.63157502E+01  8.63157502E+01  8.63157502E+01

                tmp_parmtop = str(PurePath(self.tmp_folder).joinpath("top_temp.parmtop"))
                shutil.copyfile(self.io_dict['out']['output_top_path'], tmp_parmtop)

                with open(self.io_dict['out']['output_top_path'],'w') as new_top:
                    with open(tmp_parmtop,'r') as old_top:
                        for line in old_top:
                            if 'BOX_DIMENSIONS' in line:
                                box_flag = True
                                new_top.write(line)
                            elif box_flag and 'FORMAT' not in line:
                                new_top.write(top_box_line + "\n")
                                box_flag = False
                            else:
                                new_top.write(line)

        # Remove temporary file(s)
        if self.remove_tmp:
            fu.rm(self.tmp_folder)
            fu.rm("leap.log")
            fu.log('Removed: %s' % str(self.tmp_folder), out_log)
            fu.log('Removed: leap.log', out_log)

        return returncode

def leap_add_ions(input_pdb_path: str, output_pdb_path: str,
           output_top_path: str, output_crd_path: str,
           properties: dict = None) -> int:
    """Create :class:`LeapAddIons <leap.leap_add_ions.LeapAddIons>`leap.leap_add_ions.LeapAddIons class and
    execute :meth:`launch() <leap.leap_add_ions.LeapAddIons.launch>` method"""

    return LeapAddIons( input_pdb_path=input_pdb_path,
                        output_pdb_path=output_pdb_path,
                        output_top_path=output_top_path,
                        output_crd_path=output_crd_path,
                        properties=properties).launch()

def main():
    parser = argparse.ArgumentParser(description='Adds counterions to a system box for an AMBER MD system using tLeap.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
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
    LeapAddIons(   input_pdb_path=args.input_pdb_path,
                            output_pdb_path=args.output_pdb_path,
                            output_top_path=args.output_top_path,
                            output_crd_path=args.output_crd_path,
                            properties=properties).launch()

if __name__ == '__main__':
    main()
