#!/usr/bin/env python3

"""Module containing the LeapBuildLinearStructure class and the command line interface."""

import os
import argparse
from pathlib import PurePath
from typing import List, Optional

from biobb_common.configuration import settings
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger

from biobb_amber.leap.common import _from_string_to_list, check_output_path


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
            * **container_working_dir** (*str*) - (None) Container working directory definition.
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

    def __init__(self, output_pdb_path, properties, **kwargs):
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {"in": {}, "out": {"output_pdb_path": output_pdb_path}}

        # Set default forcefields
        amber_home_path = os.getenv("AMBERHOME")
        protein_ff14SB_path = os.path.join(amber_home_path, 'dat', 'leap', 'cmd', 'leaprc.protein.ff14SB')
        dna_bsc1_path = os.path.join(amber_home_path, 'dat', 'leap', 'cmd', 'leaprc.DNA.bsc1')
        gaff_path = os.path.join(amber_home_path, 'dat', 'leap', 'cmd', 'leaprc.gaff')

        # Properties specific for BB
        self.properties = properties
        self.sequence = properties.get("sequence", "ALA GLY SER PRO ARG ALA PRO GLY")
        self.forcefield = _from_string_to_list(
            properties.get("forcefield", [protein_ff14SB_path, dna_bsc1_path, gaff_path])
        )
        # Find the paths of the leaprc files if only the force field names are provided
        self.forcefield = self.find_leaprc_paths(self.forcefield)
        self.build_library = properties.get("build_library", False)
        self.binary_path = properties.get("binary_path", "tleap")

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    def check_data_params(self, out_log, err_log):
        """Checks input/output paths correctness"""

        # Check output(s)
        self.io_dict["out"]["output_pdb_path"] = check_output_path(
            self.io_dict["out"]["output_pdb_path"],
            "output_pdb_path",
            False,
            out_log,
            self.__class__.__name__,
        )

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

    @launchlogger
    def launch(self):
        """Launches the execution of the LeapBuildLinearStructure module."""

        # check input/output paths and parameters
        self.check_data_params(self.out_log, self.err_log)

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # create .in file
        # TC5b = sequence { NASN LEU TYR ILE GLN TRP LEU LYS ASP GLY GLY PRO SER SER GLY ARG PRO PRO PRO CSER }
        # savepdb TC5b TC5b_linear.pdb
        # quit

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

        # instructions_file = str(PurePath(self.tmp_folder).joinpath("leap.in"))
        with open(instructions_file, "w") as leapin:
            # Forcefields loaded from input forcefield property
            for t in self.forcefield:
                leapin.write("source {}\n".format(t))

            leapin.write("struct = sequence {" + self.sequence + " } \n")
            leapin.write(
                "savepdb struct " + self.stage_io_dict["out"]["output_pdb_path"] + "\n"
            )
            leapin.write("quit \n")

        # Command line
        self.cmd = [self.binary_path, "-f", instructions_file_path]

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        # remove temporary folder(s)
        self.tmp_files.extend(
            [self.stage_io_dict.get("unique_dir", ""), str(self.tmp_folder), "leap.log"]
        )
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def leap_build_linear_structure(
    output_pdb_path: str, properties: Optional[dict] = None, **kwargs
) -> int:
    """Create :class:`LeapBuildLinearStructure <leap.leap_build_linear_structure.LeapBuildLinearStructure>`leap.leap_build_linear_structure.LeapBuildLinearStructure class and
    execute :meth:`launch() <leap.leap_build_linear_structure.LeapBuildLinearStructure.launch>` method"""

    return LeapBuildLinearStructure(
        output_pdb_path=output_pdb_path, properties=properties
    ).launch()


def main():
    parser = argparse.ArgumentParser(
        description="Building a linear (unfolded) 3D structure from an AA sequence.",
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999),
    )
    parser.add_argument("--config", required=False, help="Configuration file")

    # Specific args
    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument(
        "--output_pdb_path",
        required=True,
        help="Linear (unfolded) 3D structure PDB file. Accepted formats: pdb.",
    )

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call
    leap_build_linear_structure(
        output_pdb_path=args.output_pdb_path, properties=properties
    )


if __name__ == "__main__":
    main()
