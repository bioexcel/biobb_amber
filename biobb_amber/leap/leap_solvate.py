#!/usr/bin/env python3

"""Module containing the LeapSolvate class and the command line interface."""

import re
from pathlib import Path, PurePath
from typing import List, Optional

from biobb_common.generic.biobb_object import BiobbObject, launcher
from biobb_common.tools import file_utils as fu

from biobb_amber.leap.common import leaprc_files


class LeapSolvate(BiobbObject):
    """
    | biobb_amber LeapSolvate
    | Wrapper of the `AmberTools (AMBER MD Package) leap tool <https://ambermd.org/AmberTools.php>`_ module.
    | Creates and solvates a system box for an AMBER MD system using tLeap tool from the AmberTools MD package.

    Args:
        input_pdb_path (str): Input 3D structure PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/structure.leap.pdb>`_. Accepted formats: pdb (edam:format_1476).
        input_lib_path (str) (Optional): Input ligand library parameters file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/ligand.lib>`_. Accepted formats: lib (edam:format_3889), zip (edam:format_3987).
        input_frcmod_path (str) (Optional): Input ligand frcmod parameters file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/ligand.frcmod>`_. Accepted formats: frcmod (edam:format_3888), zip (edam:format_3987).
        input_params_path (str) (Optional): Additional leap parameter files to load with loadAmberParams Leap command. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/frcmod.ionsdang_spce.txt>`_. Accepted formats: in (edam:format_2330), leapin (edam:format_2330), txt (edam:format_2330), zip (edam:format_3987).
        input_prep_path (str) (Optional): Additional leap parameter files to load with loadAmberPrep Leap command. File type: input. Accepted formats: in (edam:format_2330), leapin (edam:format_2330), txt (edam:format_2330), zip (edam:format_3987).
        input_source_path (str) (Optional): Additional leap command files to load with source Leap command. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/leaprc.water.spce.txt>`_. Accepted formats: in (edam:format_2330), leapin (edam:format_2330), txt (edam:format_2330), zip (edam:format_3987).
        output_pdb_path (str): Output 3D structure PDB file matching the topology file. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.solv.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_top_path (str): Output topology file (AMBER ParmTop). File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.solv.top>`_. Accepted formats: top (edam:format_3881), parmtop (edam:format_3881), prmtop (edam:format_3881).
        output_crd_path (str): Output coordinates file (AMBER crd). File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.solv.crd>`_. Accepted formats: crd (edam:format_3878), mdcrd (edam:format_3878), inpcrd (edam:format_3878).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **forcefield** (*list*) - (["protein.ff14SB","DNA.bsc1","gaff"]) Forcefields to be used for the structure generation. Each item should be either a path to a leaprc file or a string with the leaprc file name if the force field is included with Amber (e.g. "/path/to/leaprc.protein.ff14SB" or "protein.ff14SB"). Default values: ["protein.ff14SB","DNA.bsc1","gaff"].
            * **water_type** (*str*) - ("TIP3PBOX") Water molecule parameters to be used for the topology. Values: POL3BOX, QSPCFWBOX, SPCBOX, SPCFWBOX, TIP3PBOX, TIP3PFBOX, TIP4PBOX, TIP4PEWBOX, OPCBOX, OPC3BOX, TIP5PBOX.
            * **box_type** (*str*) - ("truncated_octahedron") Type for the MD system box. Values: cubic, truncated_octahedron.
            * **ions_type** (*str*) - ("ionsjc_tip3p") Ions type. Values: ionsjc_tip3p, ionsjc_spce, ionsff99_tip3p, ions_charmm22, ionsjc_tip4pew, None.
            * **neutralise** (*bool*) - (False) Energetically neutralise the system adding the necessary counterions.
            * **iso** (*bool*) - (False) Make the box isometric.
            * **positive_ions_number** (*int*) - (0) Number of additional positive ions to include in the system box.
            * **negative_ions_number** (*int*) - (0) Number of additional negative ions to include in the system box.
            * **positive_ions_type** (*str*) - ("Na+") Type of additional positive ions to include in the system box. Values: Na+,K+.
            * **negative_ions_type** (*str*) - ("Cl-") Type of additional negative ions to include in the system box. Values: Cl-.
            * **distance_to_molecule** (*float*) - (8.0) Size for the MD system box -in Angstroms-, defined such as the minimum distance between any atom originally present in solute and the edge of the periodic box is given by this distance parameter.
            * **closeness** (*float*) - (1.0) How close, in Å, solvent ATOMs may come to solute ATOMs.
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
            from biobb_amber.leap.leap_solvate import leap_solvate
            prop = {
                'forcefield': ['protein.ff14SB'],
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
        """Launches the execution of the LeapSolvate module."""

        box_command = "solvateOct"
        if self.box_type == "cubic":
            box_command = "solvateBox"

        # Forcefield
        # source_ff_command = "source leaprc." + self.forcefield

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
            ions_command = (
                ions_command + "addions mol " + self.negative_ions_type + " 0 \n"
            )
            ions_command = (
                ions_command + "addions mol " + self.positive_ions_type + " 0 \n"
            )

        if self.negative_ions_number != 0:
            ions_command = (
                ions_command + "addions mol " + self.negative_ions_type + " " + str(self.negative_ions_number) + " \n"
            )
        if self.positive_ions_number != 0:
            ions_command = (
                ions_command + "addions mol " + self.positive_ions_type + " " + str(self.positive_ions_number) + " \n"
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

            # Ions Type
            if self.ions_type != "None":
                leapin.write("loadamberparams frcmod." + self.ions_type + "\n")

            # Additional Amber parameters
            for amber_params in amber_params_list:
                leapin.write("loadamberparams " + amber_params + "\n")

            # Additional Amber prep files
            for amber_prep in amber_prep_list:
                leapin.write("loadamberprep " + amber_prep + "\n")

            # Water Model loaded from input water_model property
            leapin.write(source_wat_command + " \n")

            # Ligand(s) libraries (if any)
            for amber_lib in ligands_lib_list:
                leapin.write("loadOff " + amber_lib + "\n")
            for amber_frcmod in ligands_frcmod_list:
                leapin.write("loadamberparams " + amber_frcmod + "\n")

            # Loading PDB file
            leapin.write(
                "mol = loadpdb " + self.stage_io_dict["in"]["input_pdb_path"] + " \n"
            )

            # Generating box + adding water molecules
            leapin.write(
                box_command + " mol " + self.water_type + " " + str(self.distance_to_molecule)
            )
            leapin.write(
                " iso " + str(self.closeness) + "\n"
            ) if self.iso else leapin.write(" " + str(self.closeness) + "\n")

            # Adding counterions
            leapin.write(ions_command)

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

        # Saving octahedron box with all decimals in PDB file. Needed for the add_ions BB.

        # Getting octahedron box from generated crd file
        with open(self.sandbox_file("output_crd_path"), "r") as file:
            for line in file:
                pass

        # Adding box as a first line in the generated pdb file with OCTBOX tag.
        # The file is replaced, not rewritten: Docker can have written it as root
        octbox = "OCTBOX " + line
        output_pdb = Path(self.sandbox_file("output_pdb_path"))
        content = output_pdb.read_text()
        output_pdb.unlink()
        output_pdb.write_text(octbox + content)


leap_solvate = launcher(LeapSolvate)

if __name__ == "__main__":
    LeapSolvate.main()
