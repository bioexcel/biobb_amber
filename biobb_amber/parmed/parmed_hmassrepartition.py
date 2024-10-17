#!/usr/bin/env python3

"""Module containing the ParmedHMassRepartition class and the command line interface."""
import argparse
from typing import Optional
from pathlib import PurePath
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_amber.parmed.common import check_input_path, check_output_path


class ParmedHMassRepartition(BiobbObject):
    """
    | biobb_amber ParmedHMassRepartition
    | Wrapper of the `AmberTools (AMBER MD Package) parmed tool <https://ambermd.org/AmberTools.php>`_ module.
    | Performs a Hydrogen Mass Repartition from an AMBER topology file using parmed tool from the AmberTools MD package.

    Args:
        input_top_path (str): Input AMBER topology file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/parmed/input.hmass.prmtop>`_. Accepted formats: top (edam:format_3881), parmtop (edam:format_3881), prmtop (edam:format_3881).
        output_top_path (str): Output topology file (AMBER ParmTop). File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/parmed/output.hmass.prmtop>`_. Accepted formats: top (edam:format_3881), parmtop (edam:format_3881), prmtop (edam:format_3881).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **binary_path** (*str*) - ("parmed") Path to the parmed executable binary.
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

            from biobb_amber.parmed.parmed_hmassrepartition import parmed_hmassrepartition
            parmed_hmassrepartition(input_top_path='/path/to/topology.top',
                            output_top_path='/path/to/newTopology.top')

    Info:
        * wrapped_software:
            * name: AmberTools parmed
            * version: >20.9
            * license: LGPL 2.1
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, input_top_path, output_top_path, properties=None, **kwargs) -> None:

        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            'in': {'input_top_path': input_top_path},
            'out': {'output_top_path': output_top_path}
        }

        # Properties specific for BB
        self.properties = properties
        self.binary_path = properties.get('binary_path', 'parmed')

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    def check_data_params(self, out_log, err_log):
        """ Checks input/output paths correctness """

        # Check input(s)
        self.io_dict["in"]["input_top_path"] = check_input_path(self.io_dict["in"]["input_top_path"], "input_top_path", False, out_log, self.__class__.__name__)

        # Check output(s)
        self.io_dict["out"]["output_top_path"] = check_output_path(self.io_dict["out"]["output_top_path"], "output_top_path", False, out_log, self.__class__.__name__)

    @launchlogger
    def launch(self):
        """Launches the execution of the ParmedHMassRepartition module."""

        # check input/output paths and parameters
        self.check_data_params(self.out_log, self.err_log)

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # Creating temporary folder & Parmed configuration (instructions) file
        if self.container_path:
            instructions_file = str(PurePath(self.stage_io_dict['unique_dir']).joinpath("parmed.in"))
            instructions_file_path = str(PurePath(self.container_volume_path).joinpath("parmed.in"))
            self.tmp_folder = None
        else:
            self.tmp_folder = fu.create_unique_dir()
            instructions_file = str(PurePath(self.tmp_folder).joinpath("parmed.in"))
            fu.log('Creating %s temporary folder' % self.tmp_folder, self.out_log)
            instructions_file_path = instructions_file

        with open(instructions_file, 'w') as parmedin:
            parmedin.write("hmassrepartition\n")
            parmedin.write("outparm " + self.stage_io_dict['out']['output_top_path'] + "\n")

        self.cmd = [self.binary_path,
                    '-p', self.stage_io_dict['in']['input_top_path'],
                    '-i', instructions_file_path,
                    '-O'  # Overwrite output files
                    ]

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


def parmed_hmassrepartition(input_top_path: str,
                            output_top_path: Optional[str] = None,
                            properties: Optional[dict] = None, **kwargs) -> int:
    """Create :class:`ParmedHMassRepartition <parmed.parmed_hmassrepartition.ParmedHMassRepartition>`parmed.parmed_hmassrepartition.ParmedHMassRepartition class and
    execute :meth:`launch() <parmed.parmed_hmassrepartition.ParmedHMassRepartition.launch>` method"""

    return ParmedHMassRepartition(input_top_path=input_top_path,
                                  output_top_path=output_top_path,
                                  properties=properties).launch()


def main():
    parser = argparse.ArgumentParser(description='Performs a Hydrogen Mass Repartition from an AMBER topology file using parmed tool from the AmberTools MD package.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_top_path', required=True, help='Input AMBER topology file. Accepted formats: top, parmtop, prmtop.')
    required_args.add_argument('--output_top_path', required=False, help='Output topology file (AMBER ParmTop). Accepted formats: top, parmtop, prmtop.')

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call
    parmed_hmassrepartition(input_top_path=args.input_top_path,
                            output_top_path=args.output_top_path,
                            properties=properties)


if __name__ == '__main__':
    main()
