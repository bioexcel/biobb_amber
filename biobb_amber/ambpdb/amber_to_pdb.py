#!/usr/bin/env python3

"""Module containing the AmberToPDB class and the command line interface."""
import argparse
import shutil
from pathlib import Path, PurePath
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_amber.ambpdb.common import *

class AmberToPDB():
    """
    | biobb_amber AmberToPDB
    | Wrapper of the `AmberTools (AMBER MD Package) ambpdb tool <https://ambermd.org/AmberTools.php>`_ module.
    | Generates a PDB structure from AMBER topology (parmtop) and coordinates (crd) files, using the ambpdb tool from the AmberTools MD package.

    Args:
        input_top_path (str): AMBER topology file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/ambpdb/structure.leap.top>`_. Accepted formats: top (edam:format_3881), parmtop (edam:format_3881), prmtop (edam:format_3881).
        input_crd_path (str): AMBER coordinates file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/ambpdb/structure.leap.crd>`_. Accepted formats: crd (edam:format_3878), mdcrd (edam:format_3878), inpcrd (edam:format_3878).
        output_pdb_path (str): Structure PDB file. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/ambpdb/structure.ambpdb.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

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

    def __init__(self, input_top_path, input_crd_path, output_pdb_path, properties: dict = None, **kwargs):
        properties = properties or {}

        # Input/Output files
        self.io_dict = {
            'in': { 'input_top_path': input_top_path,
                    'input_crd_path': input_crd_path},
            'out': { 'output_pdb_path': output_pdb_path }
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
        self.io_dict["in"]["input_crd_path"] = check_input_path(self.io_dict["in"]["input_crd_path"], "input_crd_path", False, out_log, self.__class__.__name__)

        # Check output(s)
        self.io_dict["out"]["output_pdb_path"] = check_output_path(self.io_dict["out"]["output_pdb_path"],"output_pdb_path", False, out_log, self.__class__.__name__)

    @launchlogger
    def launch(self):
        """Execute the :class:`AmberToPDB <amber.amber_to_pdb.AmberToPDB>`_ amber.amber_to_pdb.AmberToPDB object."""

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        # check input/output paths and parameters
        self.check_data_params(out_log)

        # Check the properties
        #fu.check_properties(self, self.properties)

        # Restart
        if self.restart:
            # 4. Include here all output file paths
            output_file_list = [self.io_dict['out']['output_pdb_path']]
            if fu.check_complete_files(output_file_list):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step, out_log, self.global_log)
                return 0

        # Command line
        cmd = ['ambpdb ',
               '-p', self.io_dict['in']['input_top_path'],
               '-c', self.io_dict['in']['input_crd_path'],
               '> ', self.io_dict['out']['output_pdb_path']
               ]
        fu.log('Creating command line with instructions and required arguments', out_log, self.global_log)

        # Launch execution
        returncode = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()

        # Remove temporary file(s)
        #if self.remove_tmp:
        # Nothing to remove

        return returncode

def amber_to_pdb(input_top_path: str, input_crd_path: str, output_pdb_path: str,
           properties: dict = None, **kwargs) -> int:
    """Create :class:`AmberToPDB <amber.amber_to_pdb.AmberToPDB>`amber.amber_to_pdb.AmberToPDB class and
    execute :meth:`launch() <amber.amber_to_pdb.AmberToPDB.launch>` method"""

    return AmberToPDB( input_top_path=input_top_path,
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
    AmberToPDB(input_top_path=args.input_top_path,
                input_crd_path=args.input_crd_path,
                output_pdb_path=args.output_pdb_path,
                properties=properties).launch()

if __name__ == '__main__':
    main()
