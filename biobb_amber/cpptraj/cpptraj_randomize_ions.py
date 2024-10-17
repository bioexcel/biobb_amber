#!/usr/bin/env python3

"""Module containing the CpptrajRandomizeIons class and the command line interface."""
import argparse
from typing import Optional
from pathlib import PurePath
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_amber.cpptraj.common import check_input_path, check_output_path


class CpptrajRandomizeIons(BiobbObject):
    """
    | biobb_amber.cpptraj.cpptraj_randomize_ions CpptrajRandomizeIons
    | Wrapper of the `AmberTools (AMBER MD Package) cpptraj tool <https://ambermd.org/AmberTools.php>`_ module.
    | Swap specified ions with randomly selected solvent molecules using cpptraj tool from the AmberTools MD package.

    Args:
        input_top_path (str): Input topology file (AMBER ParmTop). File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/cpptraj/structure.ions.parmtop>`_. Accepted formats: top (edam:format_3881), parmtop (edam:format_3881), prmtop (edam:format_3881).
        input_crd_path (str): Input coordinates file (AMBER crd). File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/cpptraj/structure.ions.crd>`_. Accepted formats: crd (edam:format_3878), mdcrd (edam:format_3878), inpcrd (edam:format_3878).
        output_pdb_path (str): Structure PDB file with randomized ions. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/cpptraj/structure.randIons.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_crd_path (str): Structure CRD file with coordinates including randomized ions. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/cpptraj/structure.randIons.crd>`_. Accepted formats: crd (edam:format_3878), mdcrd (edam:format_3878), inpcrd (edam:format_3878).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **ion_mask** (*str*) - (":K+,Cl-,Na+") Ions to be randomized. Cpptraj mask syntax can be found at the official `Cpptraj manual <https://amber-md.github.io/cpptraj/CPPTRAJ.xhtml>`_.
            * **solute_mask** (*str*) - (":DA,DC,DG,DT,D?3,D?5") Solute (or set of atoms) around which the ions can get no closer than the distance specified. Cpptraj mask syntax can be found at the official `Cpptraj manual <https://amber-md.github.io/cpptraj/CPPTRAJ.xhtml>`_.
            * **distance** (*float*) - (5.0) Minimum distance cutoff for the ions around the defined solute.
            * **overlap** (*float*) - (3.5) Minimum distance between ions.
            * **binary_path** (*str*) - ("cpptraj") Path to the cpptraj executable binary.
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

            from biobb_amber.cpptraj.cpptraj_randomize_ions import cpptraj_randomize_ions
            prop = {
                'remove_tmp': True
            }
            cpptraj_randomize_ions(input_top_path='/path/to/topology.top',
                          input_crd_path='/path/to/coordinates.crd',
                          output_pdb_path='/path/to/newStructure.pdb',
                          output_crd_path='/path/to/newCoordinates.crd',
                          properties=prop)

    Info:
        * wrapped_software:
            * name: AmberTools cpptraj
            * version: >20.9
            * license: LGPL 2.1
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, input_top_path: str, input_crd_path: str, output_pdb_path: str, output_crd_path: str, properties, **kwargs) -> None:

        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            'in': {
                'input_top_path': input_top_path,
                'input_crd_path': input_crd_path
            },
            'out': {
                'output_pdb_path': output_pdb_path,
                'output_crd_path': output_crd_path
            }
        }

        # Properties specific for BB
        self.properties = properties
        self.ion_mask = properties.get('ion_mask', ":K+,Cl-,Na+")
        self.solute_mask = properties.get('solute_mask', ":DA,DC,DG,DT,D?3,D?5")
        self.distance = properties.get('distance', 5.0)
        self.overlap = properties.get('overlap', 3.5)
        self.binary_path = properties.get('binary_path', 'cpptraj')

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    def check_data_params(self, out_log, err_log):
        """ Checks input/output paths correctness """

        # Check input(s)
        self.io_dict["in"]["input_top_path"] = check_input_path(self.io_dict["in"]["input_top_path"], "input_top_path", False, out_log, self.__class__.__name__)
        self.io_dict["in"]["input_crd_path"] = check_input_path(self.io_dict["in"]["input_crd_path"], "input_crd_path", False, out_log, self.__class__.__name__)

        # Check output(s)
        self.io_dict["out"]["output_pdb_path"] = check_output_path(self.io_dict["out"]["output_pdb_path"], "output_pdb_path", False, out_log, self.__class__.__name__)
        self.io_dict["out"]["output_crd_path"] = check_output_path(self.io_dict["out"]["output_crd_path"], "output_crd_path", False, out_log, self.__class__.__name__)

    @launchlogger
    def launch(self):
        """Launches the execution of the CpptrajRandomizeIons module."""

        # check input/output paths and parameters
        self.check_data_params(self.out_log, self.err_log)

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        if self.container_path:
            instructions_file = str(PurePath(self.stage_io_dict['unique_dir']).joinpath("cpptraj.in"))
            instructions_file_path = str(PurePath(self.container_volume_path).joinpath("cpptraj.in"))
        else:
            self.tmp_folder = fu.create_unique_dir()
            instructions_file = str(PurePath(self.tmp_folder).joinpath("cpptraj.in"))
            fu.log('Creating %s temporary folder' % self.tmp_folder, self.out_log)
            instructions_file_path = instructions_file

        # create cpptraj.in file
        # trajin randomizeIons.crd
        # randomizeions :K+,Cl-,Na+ around :DA,DC,DG,DT,D?3,D?5 by 5.0 overlap 3.5
        # trajout solv_randion.crd restart
        # trajout solv_randion.pdb pdb
        # go

        with open(instructions_file, 'w') as cpptrajin:
            cpptrajin.write("trajin " + self.stage_io_dict['in']['input_crd_path'] + " \n")
            cpptrajin.write("randomizeions " + self.ion_mask + " around " + self.solute_mask + " by " + str(self.distance) + " overlap " + str(self.overlap) + " \n")
            cpptrajin.write("trajout " + self.stage_io_dict['out']['output_crd_path'] + " restart \n")
            cpptrajin.write("trajout " + self.stage_io_dict['out']['output_pdb_path'] + " pdb \n")
            cpptrajin.write("go\n")

        # Command line
        self.cmd = [self.binary_path,
                    self.stage_io_dict['in']['input_top_path'],
                    '-i', instructions_file_path
                    ]

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        # Remove temporary file(s)
        self.tmp_files.extend([
            self.stage_io_dict.get("unique_dir", ""),
            self.tmp_folder,
            "cpptraj.log"
        ])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def cpptraj_randomize_ions(input_top_path: str, input_crd_path: str,
                           output_pdb_path: str, output_crd_path: str,
                           properties: Optional[dict] = None, **kwargs) -> int:
    """Create :class:`CpptrajRandomizeIons <cpptraj.cpptraj_randomize_ions.CpptrajRandomizeIons>`cpptraj.cpptraj_randomize_ions.CpptrajRandomizeIons class and
execute :meth:`launch() <cpptraj.cpptraj_randomize_ions.CpptrajRandomizeIons.launch>` method"""

    return CpptrajRandomizeIons(input_top_path=input_top_path,
                                input_crd_path=input_crd_path,
                                output_pdb_path=output_pdb_path,
                                output_crd_path=output_crd_path,
                                properties=properties).launch()


def main():
    parser = argparse.ArgumentParser(description='Swap specified ions with randomly selected solvent molecules using cpptraj tool from the AmberTools MD package.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_top_path', required=True, help='Input topology file (AMBER ParmTop). Accepted formats: top, parmtop, prmtop.')
    required_args.add_argument('--input_crd_path', required=True, help='Input coordinates file (AMBER crd). Accepted formats: crd, mdcrd, inpcrd.')
    required_args.add_argument('--output_pdb_path', required=True, help='Structure PDB file with randomized ions. Accepted formats: pdb.')
    required_args.add_argument('--output_crd_path', required=True, help='Structure CRD file with coordinates including randomized ions. Accepted formats: crd, mdcrd, inpcrd.')

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call
    cpptraj_randomize_ions(input_top_path=args.input_top_path,
                           input_crd_path=args.input_crd_path,
                           output_pdb_path=args.output_pdb_path,
                           output_crd_path=args.output_crd_path,
                           properties=properties)


if __name__ == '__main__':
    main()
