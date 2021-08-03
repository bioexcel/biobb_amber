#!/usr/bin/env python3

"""Module containing the ParmedHMassRepartition class and the command line interface."""
import argparse
import shutil, re
from pathlib import Path, PurePath
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_amber.parmed.common import *

class ParmedHMassRepartition():
    """
    | biobb_amber ParmedHMassRepartition
    | Wrapper of the `AmberTools (AMBER MD Package) parmed tool <https://ambermd.org/AmberTools.php>`_ module.
    | Performs a Hydrogen Mass Repartition from an AMBER topology file using parmed tool from the AmberTools MD package.

    Args:
        input_top_path (str): Input AMBER topology file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/parmed/input.hmass.prmtop>`_. Accepted formats: top (edam:format_3881), parmtop (edam:format_3881), prmtop (edam:format_3881).
        output_top_path (str): Output topology file (AMBER ParmTop). File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/parmed/output.hmass.prmtop>`_. Accepted formats: top (edam:format_3881), parmtop (edam:format_3881), prmtop (edam:format_3881).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

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

        # Input/Output files
        self.io_dict = {
            'in': { 'input_top_path': input_top_path },
            'out': { 'output_top_path': output_top_path }
        }

        # Properties specific for BB
        self.properties = properties

        # Properties common in all BB
        self.can_write_console_log = properties.get('can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')
        self.remove_tmp = properties.get('remove_tmp', True)
        self.restart = properties.get('restart', False)

    def check_data_params(self, out_log):
        """ Checks input/output paths correctness """

        # Check input(s)
        self.io_dict["in"]["input_top_path"] = check_input_path(self.io_dict["in"]["input_top_path"], "input_top_path", False, out_log, self.__class__.__name__)

        # Check output(s)
        self.io_dict["out"]["output_top_path"] = check_output_path(self.io_dict["out"]["output_top_path"],"output_top_path", False, out_log, self.__class__.__name__)

    @launchlogger
    def launch(self):
        """Launches the execution of the ParmedHMassRepartition module."""

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        # check input/output paths and parameters
        self.check_data_params(out_log)

        # Check the properties
        fu.check_properties(self, self.properties)

        # Restart
        if self.restart:
            output_file_list = [self.io_dict['out']['output_top_path']]
            if fu.check_complete_files(output_file_list):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step, out_log, self.global_log)
                return 0

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir()
        fu.log('Creating %s temporary folder' % self.tmp_folder, out_log)

        # Parmed configuration (instructions) file
        instructions_file = str(PurePath(self.tmp_folder).joinpath("parmed.in"))

        with open(instructions_file, 'w') as parmedin:
            parmedin.write("hmassrepartition\n")
            parmedin.write("outparm " + self.io_dict['out']['output_top_path'] + "\n")

        fu.log('Creating command line with instructions and required arguments', out_log, self.global_log)

        cmd = ['parmed',
               '-p', self.io_dict['in']['input_top_path'],
               '-i', instructions_file,
               '-O' # Overwrite output files
               ]

        # Launch execution
        returncode = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()

        # Remove temporary file(s)
        if self.remove_tmp:
            fu.rm(self.tmp_folder)
            fu.log('Removed: %s' % str(self.tmp_folder), out_log)

        return returncode

def parmed_hmassrepartition(input_top_path: str,
           output_top_path: str = None,
           properties: dict = None, **kwargs) -> int:
    """Create :class:`ParmedHMassRepartition <parmed.parmed_hmassrepartition.ParmedHMassRepartition>`parmed.parmed_hmassrepartition.ParmedHMassRepartition class and
    execute :meth:`launch() <parmed.parmed_hmassrepartition.ParmedHMassRepartition.launch>` method"""

    return ParmedHMassRepartition( input_top_path=input_top_path,
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
    parmed_hmassrepartition(   input_top_path=args.input_top_path,
                            output_top_path=args.output_top_path,
                            properties=properties)

if __name__ == '__main__':
    main()
