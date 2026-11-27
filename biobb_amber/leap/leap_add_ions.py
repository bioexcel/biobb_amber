#!/usr/bin/env python3

"""Module containing the LeapAddIons class and the command line interface."""

import os
import re
from decimal import Decimal
from pathlib import PurePath
from typing import List, Optional

from biobb_common.generic.biobb_object import BiobbObject, launcher
from biobb_common.tools import file_utils as fu

from biobb_amber.leap.common import leaprc_files


class LeapAddIons(BiobbObject):
    """
    | biobb_amber LeapAddIons
    | Wrapper of the `AmberTools (AMBER MD Package) leap tool <https://ambermd.org/AmberTools.php>`_ module.
    | Adds counterions to a system box for an AMBER MD system using tLeap tool from the AmberTools MD package.

    Args:
        input_pdb_path (str): Input 3D structure PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/structure.ions.input.pdb>`_. Accepted formats: pdb (edam:format_1476).
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
            * **neutralise** (*bool*) - (True) Energetically neutralise the system adding the necessary counterions.
            * **ionic_concentration** (*float*) - (50) Additional ionic concentration to include in the system box. Units in mM/L.
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
        super().__init__(**locals())

        # Files sourced by tleap for the forcefield property
        self.forcefield = leaprc_files(fu.str_to_list(self.forcefield), self.container_path)

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

    def _resolve_input_files(self, io_key: str, tmp_folder: str) -> List[str]:
        """Resolve an optional input (zip or single file) to the list of paths the tleap
        script must load: a zip file is unpacked into **tmp_folder**, a folder of the sandbox."""
        file_path = self.io_dict["in"][io_key]
        if file_path is None:
            return []
        if not file_path.endswith(".zip"):
            return [self.stage_io_dict["in"][io_key]]
        extracted = fu.unzip_list(self.sandbox_file(io_key), dest_dir=tmp_folder, out_log=self.out_log)
        return [self.staged_path(path) for path in extracted]

    def run(self):
        """Launches the execution of the LeapAddIons module."""

        # Water Type
        # leaprc.water.tip4pew, tip4pd, tip3p, spceb, spce, opc, fb4, fb3
        # Values: POL3BOX, QSPCFWBOX, SPCBOX, SPCFWBOX, TIP3PBOX, TIP3PFBOX, TIP4PBOX, TIP4PEWBOX, OPCBOX, OPC3BOX, TIP5PBOX.
        source_wat_command = "source leaprc.water.tip3p"
        if self.water_type == "TIP4PEWBOX":
            source_wat_command = "source leaprc.water.tip4pew"
        if self.water_type == "TIP4PBOX":
            source_wat_command = "source leaprc.water.tip4pd"
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

        # Temporary folder in the sandbox & Leap configuration (instructions) file
        tmp_folder = self.create_tmp_dir()
        instructions_file = str(PurePath(tmp_folder).joinpath("leap.in"))
        instructions_file_path = self.staged_path(instructions_file)

        ligands_lib_list = self._resolve_input_files("input_lib_path", tmp_folder)
        ligands_frcmod_list = self._resolve_input_files("input_frcmod_path", tmp_folder)
        amber_params_list = self._resolve_input_files("input_params_path", tmp_folder)
        amber_prep_list = self._resolve_input_files("input_prep_path", tmp_folder)
        leap_source_list = self._resolve_input_files("input_source_path", tmp_folder)

        # instructions_file = str(PurePath(tmp_folder).joinpath("leap.in"))
        with open(instructions_file, "w") as leapin:
            # Forcefields loaded by default:
            # Protein: ff14SB (PARM99 + frcmod.ff99SB + frcmod.parmbsc0 + OL3 for RNA)
            # leapin.write("source leaprc.protein.ff14SB \n")
            # DNA: parmBSC1 (ParmBSC1 (ff99 + bsc0 + bsc1) for DNA. Ivani et al. Nature Methods 13: 55, 2016)
            # leapin.write("source leaprc.DNA.bsc1 \n")
            # Ligands: GAFF (General Amber Force field, J. Comput. Chem. 2004 Jul 15;25(9):1157-74)
            # leapin.write("source leaprc.gaff \n")

            # Forcefields loaded from input forcefield property
            for leaprc in self.forcefield:
                leapin.write(f"source {leaprc}\n")

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

        # Truncated octahedron box: write the box of the input pdb file (OCTBOX line) in the output crd and topology files.
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
                with open(self.sandbox_file("output_crd_path")) as file:
                    lines = file.readlines()
                    crd_lines = lines[:-1]

                # Adding old box coordinates (taken from the input pdb)
                crd_lines.append(box_line)

                # The crd and topology files are replaced, not rewritten: Docker can have written them as root
                os.remove(self.sandbox_file("output_crd_path"))
                with open(self.sandbox_file("output_crd_path"), "w") as file:
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
                    # PurePath(str(tmp_folder)).joinpath("top_temp.parmtop")
                    PurePath(self.stage_io_dict["unique_dir"]).joinpath("top_temp.parmtop")
                )
                os.replace(self.sandbox_file("output_top_path"), tmp_parmtop)

                with open(self.sandbox_file("output_top_path"), "w") as new_top:
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


leap_add_ions = launcher(LeapAddIons)

if __name__ == "__main__":
    LeapAddIons.main()
