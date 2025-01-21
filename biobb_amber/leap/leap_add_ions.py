#!/usr/bin/env python3

"""Module containing the LeapAddIons class and the command line interface."""

import os
import argparse
import re
import shutil
from decimal import Decimal
from pathlib import PurePath
from typing import List, Optional

from biobb_common.configuration import settings
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger

from biobb_amber.leap.common import _from_string_to_list


class LeapAddIons(BiobbObject):
    """
    | biobb_amber LeapAddIons
    | Wrapper of the `AmberTools (AMBER MD Package) leap tool <https://ambermd.org/AmberTools.php>`_ module.
    | Adds counterions to a system box for an AMBER MD system using tLeap tool from the AmberTools MD package.

    Args:
        input_pdb_path (str): Input 3D structure PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/structure.solv.pdb>`_. Accepted formats: pdb (edam:format_1476).
        input_lib_path (str) (Optional): Input ligand library parameters file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/ligand.lib>`_. Accepted formats: lib (edam:format_3889), zip (edam:format_3987).
        input_frcmod_path (str) (Optional): Input ligand frcmod parameters file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/ligand.frcmod>`_. Accepted formats: frcmod (edam:format_3888), zip (edam:format_3987).
        input_params_path (str) (Optional): Additional leap parameter files to load with loadAmberParams Leap command. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/frcmod.ionsdang_spce.txt>`_. Accepted formats: in (edam:format_2330), leapin (edam:format_2330), txt (edam:format_2330), zip (edam:format_3987).
        input_prep_path (str) (Optional): Additional leap parameter files to load with loadAmberPrep Leap command. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/frcmod.ionsdang_spce.txt>`_. Accepted formats: in (edam:format_2330), leapin (edam:format_2330), txt (edam:format_2330), zip (edam:format_3987).
        input_source_path (str) (Optional): Additional leap command files to load with source Leap command. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/leaprc.water.spce.txt>`_. Accepted formats: in (edam:format_2330), leapin (edam:format_2330), txt (edam:format_2330), zip (edam:format_3987).
        output_pdb_path (str): Output 3D structure PDB file matching the topology file. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.ions.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_top_path (str): Output topology file (AMBER ParmTop). File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.ions.top>`_. Accepted formats: top (edam:format_3881), parmtop (edam:format_3881), prmtop (edam:format_3881).
        output_crd_path (str): Output coordinates file (AMBER crd). File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.ions.crd>`_. Accepted formats: crd  (edam:format_3878), mdcrd (edam:format_3878), inpcrd (edam:format_3878).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **forcefield** (*list*) - (["protein.ff14SB","DNA.bsc1","gaff"]) Forcefields to be used for the structure generation. Each item should be either a path to a leaprc file or a string with the leaprc file name if the force field is included with Amber (e.g. "/path/to/leaprc.protein.ff14SB" or "protein.ff14SB"). Default values: ["protein.ff14SB","DNA.bsc1","gaff"].
            * **water_type** (*str*) - ("TIP3PBOX") Water molecule parameters to be used for the topology. Values: POL3BOX, QSPCFWBOX, SPCBOX, SPCFWBOX, TIP3PBOX, TIP3PFBOX, TIP4PBOX, TIP4PEWBOX, OPCBOX, OPC3BOX, TIP5PBOX.
            * **box_type** (*str*) - ("truncated_octahedron") Type for the MD system box. Values: cubic, truncated_octahedron.
            * **ions_type** (*str*) - ("ionsjc_tip3p") Ions type. Values: ionsjc_tip3p, ionsjc_spce, ionsff99_tip3p, ions_charmm22, ionsjc_tip4pew, None.
            * **neutralise** (*bool*) - ("True") Energetically neutralise the system adding the necessary counterions.
            * **ionic_concentration** (*float*) - (50) Additional ionic concentration to include in the system box. Units in Mol/L.
            * **positive_ions_number** (*int*) - (0) Number of additional positive ions to include in the system box.
            * **negative_ions_number** (*int*) - (0) Number of additional negative ions to include in the system box.
            * **positive_ions_type** (*str*) - ("Na+") Type of additional positive ions to include in the system box. Values: Na+,K+.
            * **negative_ions_type** (*str*) - ("Cl-") Type of additional negative ions to include in the system box. Values: Cl-.
            * **binary_path** (*str*) - ("tleap") Path to the tleap executable binary.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.
            * **container_path** (*str*) - (None) Container path definition.
            * **container_image** (*str*) - ('afandiadib/ambertools:serial') Container image definition.
            * **container_volume_path** (*str*) - ('/tmp') Container volume path definition.
            * **container_working_dir** (*str*) - (None) Container working directory definition.
            * **container_user_id** (*str*) - (None) Container user_id definition.
            * **container_shell_path** (*str*) - ('/bin/bash') Path to default shell inside the container.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_amber.leap.leap_add_ions import leap_add_ions
            prop = {
                'forcefield': ['protein.ff14SB'],
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

    def __init__(
        self,
        input_pdb_path: str,
        output_pdb_path: str,
        output_top_path: str,
        output_crd_path: str,
        input_lib_path: Optional[str] = None,
        input_frcmod_path: Optional[str] = None,
        input_params_path: Optional[str] = None,
        input_prep_path: Optional[str] = None,
        input_source_path: Optional[str] = None,
        properties: Optional[dict] = None,
        **kwargs,
    ):
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            "in": {
                "input_pdb_path": input_pdb_path,
                "input_lib_path": input_lib_path,
                "input_frcmod_path": input_frcmod_path,
                "input_params_path": input_params_path,
                "input_prep_path": input_prep_path,
                "input_source_path": input_source_path,
            },
            "out": {
                "output_pdb_path": output_pdb_path,
                "output_top_path": output_top_path,
                "output_crd_path": output_crd_path,
            },
        }

        # Ligand Parameter lists
        self.ligands_lib_list = []
        if input_lib_path:
            self.ligands_lib_list.append(input_lib_path)

        self.ligands_frcmod_list = []
        if input_frcmod_path:
            self.ligands_frcmod_list.append(input_frcmod_path)

        # Set default forcefields
        amber_home_path = os.getenv("AMBERHOME")
        protein_ff14SB_path = os.path.join(amber_home_path, 'dat', 'leap', 'cmd', 'leaprc.protein.ff14SB')
        dna_bsc1_path = os.path.join(amber_home_path, 'dat', 'leap', 'cmd', 'leaprc.DNA.bsc1')
        gaff_path = os.path.join(amber_home_path, 'dat', 'leap', 'cmd', 'leaprc.gaff')

        # Properties specific for BB
        self.properties = properties
        self.forcefield = _from_string_to_list(
            properties.get("forcefield", [protein_ff14SB_path, dna_bsc1_path, gaff_path])
        )
        # Find the paths of the leaprc files if only the force field names are provided
        self.forcefield = self.find_leaprc_paths(self.forcefield)
        self.water_type = properties.get("water_type", "TIP3PBOX")
        self.box_type = properties.get("box_type", "truncated_octahedron")
        self.ions_type = properties.get("ions_type", "ionsjc_tip3p")
        self.neutralise = properties.get("neutralise", True)
        self.ionic_concentration = properties.get("ionic_concentration", 50)
        self.positive_ions_number = properties.get("positive_ions_number", 0)
        self.positive_ions_type = properties.get("positive_ions_type", "Na+")
        self.negative_ions_number = properties.get("negative_ions_number", 0)
        self.negative_ions_type = properties.get("negative_ions_type", "Cl-")
        self.binary_path = properties.get("binary_path", "tleap")

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    def find_leaprc_paths(self, forcefields: List[str]) -> List[str]:
        """
        Find the leaprc paths for the force fields provided.

        For each item in the forcefields list, the function checks if the str is a path to an existing file.
        If not, it tries to find the file in the $AMBERHOME/dat/leap/cmd/ directory or the $AMBERHOME/dat/leap/cmd/oldff/
        directory with and without the leaprc prefix.

        Args:
            forcefields (List[str]): List of force fields to find the leaprc files for.

        Returns:
            List[str]: List of leaprc file paths.
        """

        leaprc_paths = []

        for forcefield in forcefields:

            num_paths = len(leaprc_paths)

            # Check if the forcefield is a path to an existing file
            if os.path.exists(forcefield):
                leaprc_paths.append(forcefield)
                continue

            # Check if the forcefield is in the leaprc directory
            leaprc_path = os.path.join(os.environ.get('AMBERHOME', ''), 'dat', 'leap', 'cmd', f"leaprc.{forcefield}")
            if os.path.exists(leaprc_path):
                leaprc_paths.append(leaprc_path)
                continue

            # Check if the forcefield is in the oldff directory
            leaprc_path = os.path.join(os.environ.get('AMBERHOME', ''), 'dat', 'leap', 'cmd', 'oldff', f"leaprc.{forcefield}")
            if os.path.exists(leaprc_path):
                leaprc_paths.append(leaprc_path)
                continue

            # Check if the forcefield is in the leaprc directory without the leaprc prefix
            leaprc_path = os.path.join(os.environ.get('AMBERHOME', ''), 'dat', 'leap', 'cmd', f"{forcefield}")
            if os.path.exists(leaprc_path):
                leaprc_paths.append(leaprc_path)
                continue

            # Check if the forcefield is in the oldff directory without the leaprc prefix
            leaprc_path = os.path.join(os.environ.get('AMBERHOME', ''), 'dat', 'leap', 'cmd', 'oldff', f"{forcefield}")
            if os.path.exists(leaprc_path):
                leaprc_paths.append(leaprc_path)
                continue

            new_num_paths = len(leaprc_paths)

            if new_num_paths == num_paths:
                raise ValueError(f"Force field {forcefield} not found. Check the $AMBERHOME/dat/leap/cmd/ directory for available force fields or provide the path to an existing leaprc file.")

        return leaprc_paths

    # def check_data_params(self, out_log, err_log):
    #     """ Checks input/output paths correctness """

    #     # Check input(s)
    #     self.io_dict["in"]["input_pdb_path"] = check_input_path(self.io_dict["in"]["input_pdb_path"], "input_pdb_path", False, out_log, self.__class__.__name__)
    #     self.io_dict["in"]["input_lib_path"] = check_input_path(self.io_dict["in"]["input_lib_path"], "input_lib_path", True, out_log, self.__class__.__name__)
    #     self.io_dict["in"]["input_frcmod_path"] = check_input_path(self.io_dict["in"]["input_frcmod_path"], "input_frcmod_path", True, out_log, self.__class__.__name__)
    #     # self.io_dict["in"]["input_params_path"] = check_input_path(self.io_dict["in"]["input_params_path"], "input_params_path", True, out_log, self.__class__.__name__)
    #     # self.io_dict["in"]["input_source_path"] = check_input_path(self.io_dict["in"]["input_source_path"], "input_source_path", True, out_log, self.__class__.__name__)

    #     # Check output(s)
    #     self.io_dict["out"]["output_pdb_path"] = check_output_path(self.io_dict["out"]["output_pdb_path"], "output_pdb_path", False, out_log, self.__class__.__name__)
    #     self.io_dict["out"]["output_top_path"] = check_output_path(self.io_dict["out"]["output_top_path"], "output_top_path", False, out_log, self.__class__.__name__)
    #     self.io_dict["out"]["output_crd_path"] = check_output_path(self.io_dict["out"]["output_crd_path"], "output_crd_path", False, out_log, self.__class__.__name__)

    def find_out_number_of_ions(self):
        """Computes the number of positive and negative ions from the input ionic
        concentration and the number of water molecules in the system box."""

        # Finding number of water molecules in the box
        cnt = 0
        with open(self.io_dict["in"]["input_pdb_path"]) as fp:
            for line in fp:
                # Water molecules are identified with different resids
                # by different forcefields / MD packages
                pq = re.compile((r"WAT|HOH|TP3|TIP3|SOL"), re.M)
                if pq.search(line):
                    # Incrementing number of water molecules just in the water
                    # oxygen atom, ignoring hydrogen or dummy atoms
                    pq2 = re.compile(r"H|EPW|EP1|EP2", re.M)
                    if not pq2.search(line):
                        cnt = cnt + 1

        # To get to X mM ions we need
        # n(NaCl) = #waters / 55 Mol * X M
        # where X M = X mM / 1000
        self.nio = int((cnt / 55) * (self.ionic_concentration / 1000))

    @launchlogger
    def launch(self):
        """Launches the execution of the LeapAddIons module."""

        # check input/output paths and parameters
        # self.check_data_params(self.out_log, self.err_log)

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

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
            # ions_command = ions_command + "addions mol " + self.negative_ions_type + " 0 \n"
            # ions_command = ions_command + "addions mol " + self.positive_ions_type + " 0 \n"
            ions_command = (
                ions_command + "addionsRand mol " + self.negative_ions_type + " 0 \n"
            )
            ions_command = (
                ions_command + "addionsRand mol " + self.positive_ions_type + " 0 \n"
            )

        if (
            self.ionic_concentration and self.negative_ions_number == 0 and self.positive_ions_number == 0
        ):
            self.find_out_number_of_ions()
            nneg = self.nio  # Update with function
            npos = self.nio  # Update with function
            # ions_command = ions_command + "addions mol " + self.negative_ions_type + " " + str(nneg) + " \n"
            # ions_command = ions_command + "addions mol " + self.positive_ions_type + " " + str(npos) + " \n"
            ions_command = (
                ions_command + "addionsRand mol " + self.negative_ions_type + " " + str(nneg) + " \n"
            )
            ions_command = (
                ions_command + "addionsRand mol " + self.positive_ions_type + " " + str(npos) + " \n"
            )
        else:
            if self.negative_ions_number != 0:
                # ions_command = ions_command + "addions mol " + self.negative_ions_type + " " + str(self.negative_ions_number) + " \n"
                ions_command = (
                    ions_command + "addionsRand mol " + self.negative_ions_type + " " + str(self.negative_ions_number) + " \n"
                )
            if self.positive_ions_number != 0:
                # ions_command = ions_command + "addions mol " + self.positive_ions_type + " " + str(self.positive_ions_number) + " \n"
                ions_command = (
                    ions_command + "addionsRand mol " + self.positive_ions_type + " " + str(self.positive_ions_number) + " \n"
                )

        # Creating temporary folder & Leap configuration (instructions) file
        if self.container_path:
            instructions_file = str(
                PurePath(self.stage_io_dict["unique_dir"]).joinpath("leap.in")
            )
            instructions_file_path = str(
                PurePath(self.container_volume_path).joinpath("leap.in")
            )
            self.tmp_folder = None
        else:
            self.tmp_folder = fu.create_unique_dir()
            instructions_file = str(PurePath(self.tmp_folder).joinpath("leap.in"))
            fu.log("Creating %s temporary folder" % self.tmp_folder, self.out_log)
            instructions_file_path = instructions_file

        ligands_lib_list = []
        if self.io_dict["in"]["input_lib_path"] is not None:
            if self.io_dict["in"]["input_lib_path"].endswith(".zip"):
                ligands_lib_list = fu.unzip_list(
                    self.stage_io_dict["in"]["input_lib_path"],
                    dest_dir=self.tmp_folder,
                    out_log=self.out_log,
                )
            else:
                ligands_lib_list.append(self.stage_io_dict["in"]["input_lib_path"])

        ligands_frcmod_list = []
        if self.io_dict["in"]["input_frcmod_path"] is not None:
            if self.io_dict["in"]["input_frcmod_path"].endswith(".zip"):
                ligands_frcmod_list = fu.unzip_list(
                    self.stage_io_dict["in"]["input_frcmod_path"],
                    dest_dir=self.tmp_folder,
                    out_log=self.out_log,
                )
            else:
                ligands_frcmod_list.append(
                    self.stage_io_dict["in"]["input_frcmod_path"]
                )

        amber_params_list = []
        if self.io_dict["in"]["input_params_path"] is not None:
            if self.io_dict["in"]["input_params_path"].endswith(".zip"):
                amber_params_list = fu.unzip_list(
                    self.stage_io_dict["in"]["input_params_path"],
                    dest_dir=self.tmp_folder,
                    out_log=self.out_log,
                )
            else:
                amber_params_list.append(self.stage_io_dict["in"]["input_params_path"])

        amber_prep_list = []
        if self.io_dict["in"]["input_prep_path"] is not None:
            if self.io_dict["in"]["input_prep_path"].endswith(".zip"):
                amber_prep_list = fu.unzip_list(
                    self.stage_io_dict["in"]["input_prep_path"],
                    dest_dir=self.tmp_folder,
                    out_log=self.out_log,
                )
            else:
                amber_prep_list.append(self.stage_io_dict["in"]["input_prep_path"])

        leap_source_list = []
        if self.io_dict["in"]["input_source_path"] is not None:
            if self.io_dict["in"]["input_source_path"].endswith(".zip"):
                leap_source_list = fu.unzip_list(
                    self.stage_io_dict["in"]["input_source_path"],
                    dest_dir=self.tmp_folder,
                    out_log=self.out_log,
                )
            else:
                leap_source_list.append(self.stage_io_dict["in"]["input_source_path"])

        # instructions_file = str(PurePath(self.tmp_folder).joinpath("leap.in"))
        with open(instructions_file, "w") as leapin:
            # Forcefields loaded by default:
            # Protein: ff14SB (PARM99 + frcmod.ff99SB + frcmod.parmbsc0 + OL3 for RNA)
            # leapin.write("source leaprc.protein.ff14SB \n")
            # DNA: parmBSC1 (ParmBSC1 (ff99 + bsc0 + bsc1) for DNA. Ivani et al. Nature Methods 13: 55, 2016)
            # leapin.write("source leaprc.DNA.bsc1 \n")
            # Ligands: GAFF (General Amber Force field, J. Comput. Chem. 2004 Jul 15;25(9):1157-74)
            # leapin.write("source leaprc.gaff \n")

            # Forcefields loaded from input forcefield property
            for t in self.forcefield:
                leapin.write("source {}\n".format(t))

            # Additional Leap commands
            for leap_commands in leap_source_list:
                leapin.write("source " + leap_commands + "\n")

            # Water Model loaded from input water_model property
            leapin.write(source_wat_command + " \n")

            # Ions Type
            if self.ions_type != "None":
                leapin.write("loadamberparams frcmod." + self.ions_type + "\n")

            # Additional Amber parameters
            for amber_params in amber_params_list:
                leapin.write("loadamberparams " + amber_params + "\n")

            # Additional Amber prep files
            for amber_prep in amber_prep_list:
                leapin.write("loadamberprep " + amber_prep + "\n")

            # Ligand(s) libraries (if any)
            for amber_lib in ligands_lib_list:
                leapin.write("loadOff " + amber_lib + "\n")
            for amber_frcmod in ligands_frcmod_list:
                leapin.write("loadamberparams " + amber_frcmod + "\n")

            # Loading PDB file
            leapin.write(
                "mol = loadpdb " + self.stage_io_dict["in"]["input_pdb_path"] + " \n"
            )

            # Adding ions
            leapin.write(ions_command)

            # Generating box
            leapin.write("setBox mol vdw \n")

            # Saving output PDB file, coordinates and topology
            leapin.write(
                "savepdb mol " + self.stage_io_dict["out"]["output_pdb_path"] + " \n"
            )
            leapin.write(
                "saveAmberParm mol " + self.stage_io_dict["out"]["output_top_path"] + " " + self.stage_io_dict["out"]["output_crd_path"] + "\n"
            )
            leapin.write("quit \n")

        # Command line
        self.cmd = [self.binary_path, "-f", instructions_file_path]

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        if self.box_type != "cubic":
            fu.log(
                "Fixing truncated octahedron Box in the topology and coordinates files",
                self.out_log,
                self.global_log,
            )

            # Taking box info from input PDB file, CRYST1 tag (first line)
            with open(self.io_dict["in"]["input_pdb_path"]) as file:
                lines = file.readlines()
                pdb_line = lines[0]

            if "OCTBOX" not in pdb_line:
                fu.log(
                    "WARNING: box info not found in input PDB file (OCTBOX). Needed to correctly assign the octahedron box. Assuming cubic box.",
                    self.out_log,
                    self.global_log,
                )
            else:
                # PDB info: CRYST1   86.316   86.316   86.316 109.47 109.47 109.47 P 1
                # PDB info: OCTBOX   86.1942924  86.1942924  86.1942924 109.4712190 109.4712190 109.4712190
                # regex_box = 'CRYST1\s*(\d+\.\d+)\s*(\d+\.\d+)\s*(\d+\.\d+)\s*(\d+\.\d+)\s*(\d+\.\d+)\s*(\d+\.\d+)\s*P 1'
                regex_box = r"OCTBOX\s*(\d+\.\d+)\s*(\d+\.\d+)\s*(\d+\.\d+)\s*(\d+\.\d+)\s*(\d+\.\d+)\s*(\d+\.\d+)"
                box = re.findall(regex_box, pdb_line)[0]
                box_line = ""
                for coord in box:
                    box_line += "{:12.7f}".format(float(coord))

                # PRMTOP info: 1.09471219E+02  8.63157502E+01  8.63157502E+01  8.63157502E+01
                top_box_line = ""
                top_box_line += "  %.8E" % Decimal(float(box[3]))
                top_box_line += "  %.8E" % Decimal(float(box[0]))
                top_box_line += "  %.8E" % Decimal(float(box[1]))
                top_box_line += "  %.8E" % Decimal(float(box[2]))

                # Removing box generated by tleap from the crd file (last line)
                with open(self.io_dict["out"]["output_crd_path"]) as file:
                    lines = file.readlines()
                    crd_lines = lines[:-1]

                # Adding old box coordinates (taken from the input pdb)
                crd_lines.append(box_line)

                with open(self.io_dict["out"]["output_crd_path"], "w") as file:
                    for line in crd_lines:
                        file.write(str(line))
                    file.write("\n")

                # Now fixing IFBOX param in prmtop.
                box_flag = False
                ifbox_flag = 0
                # %FLAG BOX_DIMENSIONS
                # %FORMAT(5E16.8)
                # 1.09471219E+02  8.63157502E+01  8.63157502E+01  8.63157502E+01

                tmp_parmtop = str(
                    PurePath(str(self.tmp_folder)).joinpath("top_temp.parmtop")
                )
                shutil.copyfile(self.io_dict["out"]["output_top_path"], tmp_parmtop)

                with open(self.io_dict["out"]["output_top_path"], "w") as new_top:
                    with open(tmp_parmtop, "r") as old_top:
                        for line in old_top:
                            if "BOX_DIMENSIONS" in line:
                                box_flag = True
                                new_top.write(line)
                            elif box_flag and "FORMAT" not in line:
                                new_top.write(top_box_line + "\n")
                                box_flag = False
                            elif (
                                "FLAG POINTERS" in line or ifbox_flag == 1 or ifbox_flag == 2 or ifbox_flag == 3
                            ):
                                ifbox_flag += 1
                                new_top.write(line)
                            elif ifbox_flag == 4:
                                # new_top.write(top_box_line + "\n")
                                new_top.write(line[:56] + "       2" + line[64:])
                                ifbox_flag += 1
                            else:
                                new_top.write(line)

        # remove temporary folder(s)
        self.tmp_files.extend(
            [self.stage_io_dict.get("unique_dir", ""), str(self.tmp_folder), "leap.log"]
        )
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def leap_add_ions(
    input_pdb_path: str,
    output_pdb_path: str,
    output_top_path: str,
    output_crd_path: str,
    input_lib_path: Optional[str] = None,
    input_frcmod_path: Optional[str] = None,
    input_params_path: Optional[str] = None,
    input_prep_path: Optional[str] = None,
    input_source_path: Optional[str] = None,
    properties: Optional[dict] = None,
    **kwargs,
) -> int:
    """Create :class:`LeapAddIons <leap.leap_add_ions.LeapAddIons>`leap.leap_add_ions.LeapAddIons class and
    execute :meth:`launch() <leap.leap_add_ions.LeapAddIons.launch>` method"""

    return LeapAddIons(
        input_pdb_path=input_pdb_path,
        input_lib_path=input_lib_path,
        input_frcmod_path=input_frcmod_path,
        input_params_path=input_params_path,
        input_prep_path=input_prep_path,
        input_source_path=input_source_path,
        output_pdb_path=output_pdb_path,
        output_top_path=output_top_path,
        output_crd_path=output_crd_path,
        properties=properties,
    ).launch()


def main():
    parser = argparse.ArgumentParser(
        description="Adds counterions to a system box for an AMBER MD system using tLeap.",
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999),
    )
    parser.add_argument("--config", required=False, help="Configuration file")

    # Specific args
    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument(
        "--input_pdb_path",
        required=True,
        help="Input 3D structure PDB file. Accepted formats: pdb.",
    )
    required_args.add_argument(
        "--input_lib_path",
        required=False,
        help="Input ligand library parameters file. Accepted formats: lib, zip.",
    )
    required_args.add_argument(
        "--input_frcmod_path",
        required=False,
        help="Input ligand frcmod parameters file. Accepted formats: frcmod, zip.",
    )
    required_args.add_argument(
        "--input_params_path",
        required=False,
        help="Additional leap parameter files to load with loadAmberParams Leap command. Accepted formats: leapin, in, txt, zip.",
    )
    required_args.add_argument(
        "--input_prep_path",
        required=False,
        help="Additional leap parameter files to load with loadAmberPrep Leap command. Accepted formats: leapin, in, txt, zip.",
    )
    required_args.add_argument(
        "--input_source_path",
        required=False,
        help="Additional leap command files to load with source Leap command. Accepted formats: leapin, in, txt, zip.",
    )
    required_args.add_argument(
        "--output_pdb_path",
        required=True,
        help="Output 3D structure PDB file matching the topology file. Accepted formats: pdb.",
    )
    required_args.add_argument(
        "--output_top_path",
        required=True,
        help="Output topology file (AMBER ParmTop). Accepted formats: top.",
    )
    required_args.add_argument(
        "--output_crd_path",
        required=True,
        help="Output coordinates file (AMBER crd). Accepted formats: crd.",
    )

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call
    leap_add_ions(
        input_pdb_path=args.input_pdb_path,
        input_lib_path=args.input_lib_path,
        input_frcmod_path=args.input_frcmod_path,
        input_params_path=args.input_params_path,
        input_prep_path=args.input_prep_path,
        input_source_path=args.input_source_path,
        output_pdb_path=args.output_pdb_path,
        output_top_path=args.output_top_path,
        output_crd_path=args.output_crd_path,
        properties=properties,
    )


if __name__ == "__main__":
    main()
