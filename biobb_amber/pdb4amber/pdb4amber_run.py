#!/usr/bin/env python3

"""Module containing the Pdb4amber class and the command line interface."""
import argparse
from typing import Optional
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_amber.pdb4amber.common import check_input_path, check_output_path


class Pdb4amberRun(BiobbObject):
    """
    | biobb_amber.pdb4amber.pdb4amber_run Pdb4amberRun
    | Wrapper of the `AmberTools (AMBER MD Package) pdb4amber tool <https://ambermd.org/AmberTools.php>`_ module.
    | Analyse PDB files and clean them for further usage, especially with the LEaP programs of Amber, using pdb4amber tool from the AmberTools MD package.

    Args:
        input_pdb_path (str): Input 3D structure PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pdb4amber/1aki_fixed.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_pdb_path (str): Output 3D structure PDB file. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/pdb4amber/structure.pdb4amber.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **remove_hydrogens** (*bool*) - (False) Remove hydrogen atoms from the PDB file.
            * **remove_waters** (*bool*) - (False) Remove water molecules from the PDB file.
            * **constant_pH** (*bool*) - (False) Rename ionizable residues e.g. GLU,ASP,HIS for constant pH simulation.
            * **reduce** (*bool*) - (False) Run Reduce first to add hydrogen atoms.
            * **binary_path** (*str*) - ("pdb4amber") Path to the pdb4amber executable binary.
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

            from biobb_amber.pdb4amber.pdb4amber_run import pdb4amber_run
            prop = {
                'remove_tmp': True
            }
            pdb4amber_run(input_pdb_path='/path/to/structure.pdb',
                          output_pdb_path='/path/to/newStructure.pdb',
                          properties=prop)

    Info:
        * wrapped_software:
            * name: AmberTools pdb4amber
            * version: >20.9
            * license: LGPL 2.1
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, input_pdb_path: str, output_pdb_path: str, properties: Optional[dict], **kwargs):

        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            'in': {'input_pdb_path': input_pdb_path},
            'out': {'output_pdb_path': output_pdb_path}
        }

        # Properties specific for BB
        self.properties = properties
        self.remove_hydrogens = properties.get('remove_hydrogens', False)
        self.remove_waters = properties.get('remove_waters', False)
        self.constant_pH = properties.get('constant_pH', False)
        self.reduce = properties.get('reduce', False)
        self.binary_path = properties.get('binary_path', 'pdb4amber')

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    def check_data_params(self, out_log, err_log):
        """ Checks input/output paths correctness """

        # Check input(s)
        self.io_dict["in"]["input_pdb_path"] = check_input_path(self.io_dict["in"]["input_pdb_path"], "input_pdb_path", False, out_log, self.__class__.__name__)

        # Check output(s)
        self.io_dict["out"]["output_pdb_path"] = check_output_path(self.io_dict["out"]["output_pdb_path"], "output_pdb_path", False, out_log, self.__class__.__name__)

    @launchlogger
    def launch(self):
        """Launches the execution of the Pdb4amberRun module."""

        # check input/output paths and parameters
        self.check_data_params(self.out_log, self.err_log)

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir()
        fu.log('Creating %s temporary folder' % self.tmp_folder, self.out_log)

        # Command line
        # sander -O -i mdin/min.mdin -p $1.cpH.prmtop -c ph$i/$1.inpcrd -r ph$i/$1.min.rst7 -o ph$i/$1.min.o
        self.cmd = [self.binary_path,
                    '-i', self.stage_io_dict['in']['input_pdb_path'],
                    '-o', self.stage_io_dict['out']['output_pdb_path']
                    ]

        if self.remove_hydrogens:
            self.cmd.append("-y ")
        if self.remove_waters:
            self.cmd.append("-d ")
        if self.constant_pH:
            self.cmd.append("--constantph ")
        if self.reduce:
            self.cmd.append("--reduce ")

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        # remove temporary folder(s)
        self.tmp_files.extend([
            self.stage_io_dict.get("unique_dir", ""),
            str(self.tmp_folder)
        ])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def pdb4amber_run(input_pdb_path: str, output_pdb_path: str,
                  properties: Optional[dict] = None, **kwargs) -> int:
    """Create :class:`Pdb4amberRun <pdb4amber.pdb4amber_run.Pdb4amberRun>`pdb4amber.pdb4amber_run.Pdb4amberRun class and
    execute :meth:`launch() <pdb4amber.pdb4amber_run.Pdb4amberRun.launch>` method"""

    return Pdb4amberRun(input_pdb_path=input_pdb_path,
                        output_pdb_path=output_pdb_path,
                        properties=properties).launch()


def main():
    parser = argparse.ArgumentParser(description='Analyse PDB files and clean them for further usage, especially with the LEaP programs of Amber, using pdb4amber tool from the AmberTools MD package.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_pdb_path', required=True, help='Input 3D structure PDB file. Accepted formats: pdb.')
    required_args.add_argument('--output_pdb_path', required=True, help='Output 3D structure PDB file. Accepted formats: pdb.')

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call
    pdb4amber_run(input_pdb_path=args.input_pdb_path,
                  output_pdb_path=args.output_pdb_path,
                  properties=properties)


if __name__ == '__main__':
    main()
