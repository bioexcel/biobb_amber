#!/usr/bin/env python3

"""Module containing the LeapGenTop class and the command line interface."""

import os
from pathlib import PurePath
from typing import List, Optional

from biobb_common.generic.biobb_object import BiobbObject, launcher
from biobb_common.tools import file_utils as fu


class LeapGenTop(BiobbObject):
    """
    | biobb_amber.leap.leap_gen_top LeapGenTop
    | Wrapper of the `AmberTools (AMBER MD Package) leap tool <https://ambermd.org/AmberTools.php>`_ module.
    | Generates a MD topology from a molecule structure using tLeap tool from the AmberTools MD package.

    Args:
        input_pdb_path (str): Input 3D structure PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/structure.leapin.pdb>`_. Accepted formats: pdb (edam:format_1476).
        input_lib_path (str) (Optional): Input ligand library parameters file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/ligand.lib>`_. Accepted formats: lib (edam:format_3889), zip (edam:format_3987).
        input_frcmod_path (str) (Optional): Input ligand frcmod parameters file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/ligand.frcmod>`_. Accepted formats: frcmod (edam:format_3888), zip (edam:format_3987).
        input_params_path (str) (Optional): Additional leap parameter files to load with loadAmberParams Leap command. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/frcmod.ionsdang_spce.txt>`_. Accepted formats: in (edam:format_2330), leapin (edam:format_2330), txt (edam:format_2330), zip (edam:format_3987).
        input_prep_path (str) (Optional): Additional leap parameter files to load with loadAmberPrep Leap command. File type: input. Accepted formats: in (edam:format_2330), leapin (edam:format_2330), txt (edam:format_2330), zip (edam:format_3987).
        input_source_path (str) (Optional): Additional leap command files to load with source Leap command. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/leaprc.water.spce.txt>`_. Accepted formats: in (edam:format_2330), leapin (edam:format_2330), txt (edam:format_2330), zip (edam:format_3987).
        output_pdb_path (str): Output 3D structure PDB file matching the topology file. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.leap.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_top_path (str): Output topology file (AMBER ParmTop). File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.leap.top>`_. Accepted formats: top (edam:format_3881), parmtop (edam:format_3881), prmtop (edam:format_3881).
        output_crd_path (str): Output coordinates file (AMBER crd). File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.leap.crd>`_. Accepted formats: crd  (edam:format_3878), mdcrd (edam:format_3878), inpcrd (edam:format_3878).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **forcefield** (*list*) - (["protein.ff14SB","DNA.bsc1","gaff"]) Forcefields to be used for the structure generation. Each item should be either a path to a leaprc file or a string with the leaprc file name if the force field is included with Amber (e.g. "/path/to/leaprc.protein.ff14SB" or "protein.ff14SB"). Default values: ["protein.ff14SB","DNA.bsc1","gaff"].
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

        # # Ligand Parameter lists
        # self.ligands_lib_list = []
        # if input_lib_path:
        #     self.ligands_lib_list.append(input_lib_path)
        #
        # self.ligands_frcmod_list = []
        # if input_frcmod_path:
        #     self.ligands_frcmod_list.append(input_frcmod_path)

        # Set default forcefields
        if self.container_path:
            # self.forcefield = "leaprc.protein.ff14SB"
            self.forcefield = fu.str_to_list(self.forcefield)
        else:
            amber_home_path = os.getenv("AMBERHOME", "")
            protein_ff14SB_path = os.path.join(amber_home_path, 'dat', 'leap', 'cmd', 'leaprc.protein.ff14SB')
            dna_bsc1_path = os.path.join(amber_home_path, 'dat', 'leap', 'cmd', 'leaprc.DNA.bsc1')
            gaff_path = os.path.join(amber_home_path, 'dat', 'leap', 'cmd', 'leaprc.gaff')

            self.forcefield = fu.str_to_list(self.properties.get("forcefield", [protein_ff14SB_path, dna_bsc1_path, gaff_path]))
            # Find the paths of the leaprc files if only the force field names are provided
            self.forcefield = self.find_leaprc_paths(self.forcefield)

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
        """Launches the execution of the LeapGenTop module."""

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
            for t in self.forcefield:
                if self.container_path:
                    leapin.write("source leaprc.{}\n".format(t))
                else:
                    leapin.write("source {}\n".format(t))

            # Additional Leap commands
            for leap_commands in leap_source_list:
                leapin.write("source " + leap_commands + "\n")

            # Additional Amber parameters
            for amber_params in amber_params_list:
                leapin.write("loadamberparams " + amber_params + "\n")

            # Additional Amber prep files
            for amber_prep in amber_prep_list:
                leapin.write("loadamberprep " + amber_prep + "\n")

            # Ions libraries
            leapin.write("loadOff atomic_ions.lib \n")

            # Ligand(s) libraries (if any)
            for amber_lib in ligands_lib_list:
                leapin.write("loadOff " + amber_lib + "\n")
            for amber_frcmod in ligands_frcmod_list:
                leapin.write("loadamberparams " + amber_frcmod + "\n")

            # Loading PDB file
            leapin.write(
                "mol = loadpdb " + self.stage_io_dict["in"]["input_pdb_path"] + " \n"
            )

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


leap_gen_top = launcher(LeapGenTop)

if __name__ == "__main__":
    LeapGenTop.main()
