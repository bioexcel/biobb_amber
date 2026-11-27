#!/usr/bin/env python3

"""Module containing the LeapBuildLinearStructure class and the command line interface."""

from pathlib import PurePath
from typing import Optional

from biobb_common.generic.biobb_object import BiobbObject, launcher
from biobb_common.tools import file_utils as fu

from biobb_amber.leap.common import leaprc_files


class LeapBuildLinearStructure(BiobbObject):
    """
    | biobb_amber.leap.leap_build_linear_structure LeapBuildLinearStructure
    | Wrapper of the `AmberTools (AMBER MD Package) leap tool <https://ambermd.org/AmberTools.php>`_ module.
    | Builds a linear (unfolded) 3D structure from an AA sequence using tLeap tool from the AmberTools MD package.

    Args:
        output_pdb_path (str): Linear (unfolded) 3D structure PDB file. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **sequence** (*str*) - ("ALA GLY SER PRO ARG ALA PRO GLY") Aminoacid sequence to convert to a linear 3D structure. Aminoacids should be written in 3-letter code, with a blank space between them.
            * **forcefield** (*list*) - (["protein.ff14SB","DNA.bsc1","gaff"]) Forcefields to be used for the structure generation. Each item should be either a path to a leaprc file or a string with the leaprc file name if the force field is included with Amber (e.g. "/path/to/leaprc.protein.ff14SB" or "protein.ff14SB"). Default values: ["protein.ff14SB","DNA.bsc1","gaff"].
            * **build_library** (*bool*) - (False) Generate AMBER lib file for the structure.
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

    def __init__(self, output_pdb_path: str, properties: Optional[dict] = None, **kwargs):
        super().__init__(**locals())

        # Files sourced by tleap for the forcefield property
        self.forcefield = leaprc_files(fu.str_to_list(self.forcefield), self.container_path)

    def run(self):
        """Launches the execution of the LeapBuildLinearStructure module."""

        # create .in file
        # TC5b = sequence { NASN LEU TYR ILE GLN TRP LEU LYS ASP GLY GLY PRO SER SER GLY ARG PRO PRO PRO CSER }
        # savepdb TC5b TC5b_linear.pdb
        # quit

        # Temporary folder in the sandbox & Leap configuration (instructions) file
        tmp_folder = self.create_tmp_dir()
        instructions_file = str(PurePath(tmp_folder).joinpath("leap.in"))
        instructions_file_path = self.staged_path(instructions_file)

        # instructions_file = str(PurePath(tmp_folder).joinpath("leap.in"))
        with open(instructions_file, "w") as leapin:
            # Forcefields loaded from input forcefield property
            for leaprc in self.forcefield:
                leapin.write(f"source {leaprc}\n")

            leapin.write("struct = sequence {" + self.sequence + " } \n")
            leapin.write(
                "savepdb struct " + self.stage_io_dict["out"]["output_pdb_path"] + "\n"
            )
            leapin.write("quit \n")

        # Command line
        self.cmd = [self.binary_path, "-f", instructions_file_path]

        # Run Biobb block
        self.run_biobb()


leap_build_linear_structure = launcher(LeapBuildLinearStructure)

if __name__ == "__main__":
    LeapBuildLinearStructure.main()
