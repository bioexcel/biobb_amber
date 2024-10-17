#!/usr/bin/env python3

"""Module containing the AmberToPDB class and the command line interface."""
import argparse
from typing import Optional
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools.file_utils import launchlogger
from biobb_amber.ambpdb.common import check_input_path, check_output_path


class AmberToPDB(BiobbObject):
    """
    | biobb_amber AmberToPDB
    | Wrapper of the `AmberTools (AMBER MD Package) ambpdb tool <https://ambermd.org/AmberTools.php>`_ module.
    | Generates a PDB structure from AMBER topology (parmtop) and coordinates (crd) files, using the ambpdb tool from the AmberTools MD package.

    Args:
        input_top_path (str): AMBER topology file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/ambpdb/structure.leap.top>`_. Accepted formats: top (edam:format_3881), parmtop (edam:format_3881), prmtop (edam:format_3881).
        input_crd_path (str): AMBER coordinates file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/ambpdb/structure.leap.crd>`_. Accepted formats: crd (edam:format_3878), mdcrd (edam:format_3878), inpcrd (edam:format_3878), rst (edam:format_3886).
        output_pdb_path (str): Structure PDB file. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/ambpdb/structure.ambpdb.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **binary_path** (*str*) - ("ambpdb") Path to the ambpdb executable binary.
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

            from biobb_amber.ambpdb.amber_to_pdb import amber_to_pdb
            prop = {
                'remove_tmp': True
            }
            amber_to_pdb(input_top_path='/path/to/topology.top',
                          input_crd_path='/path/to/coordinates.crd',
                          output_pdb_path='/path/to/newStructure.pdb',
                          properties=prop)

    Info:
        * wrapped_software:
            * name: AmberTools ambpdb
            * version: >20.9
            * license: LGPL 2.1
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, input_top_path, input_crd_path, output_pdb_path, properties: Optional[dict] = None, **kwargs):
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            'in': {'input_top_path': input_top_path,
                   'input_crd_path': input_crd_path},
            'out': {'output_pdb_path': output_pdb_path}
        }

        # Properties specific for BB
        self.properties = properties
        self.binary_path = properties.get('binary_path', 'ambpdb')

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

    @launchlogger
    def launch(self):

        # check input/output paths and parameters
        self.check_data_params(self.out_log, self.err_log)

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # Command line
        self.cmd = [self.binary_path,
                    '-p', self.stage_io_dict['in']['input_top_path'],
                    '-c', self.stage_io_dict['in']['input_crd_path'],
                    '> ', self.stage_io_dict['out']['output_pdb_path']
                    ]

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        # Remove temporary file(s)
        self.tmp_files.extend([
            self.stage_io_dict.get("unique_dir", "")
        ])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def amber_to_pdb(input_top_path: str, input_crd_path: str, output_pdb_path: str,
                 properties: Optional[dict] = None, **kwargs) -> int:
    """Create :class:`AmberToPDB <amber.amber_to_pdb.AmberToPDB>`amber.amber_to_pdb.AmberToPDB class and
    execute :meth:`launch() <amber.amber_to_pdb.AmberToPDB.launch>` method"""

    return AmberToPDB(input_top_path=input_top_path,
                      input_crd_path=input_crd_path,
                      output_pdb_path=output_pdb_path,
                      properties=properties).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description='Generates a PDB structure from AMBER topology (parmtop) and coordinates (crd) files, using the ambpdb tool from the AmberTools MD package.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_top_path', required=True, help='AMBER topology file. Accepted formats: top, parmtop, prmtop.')
    required_args.add_argument('--input_crd_path', required=True, help='AMBER coordinates file. Accepted formats: crd, mdcrd, inpcrd.')
    required_args.add_argument('--output_pdb_path', required=True, help='Structure PDB file. Accepted formats: pdb.')

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call
    amber_to_pdb(input_top_path=args.input_top_path,
                 input_crd_path=args.input_crd_path,
                 output_pdb_path=args.output_pdb_path,
                 properties=properties)


if __name__ == '__main__':
    main()
