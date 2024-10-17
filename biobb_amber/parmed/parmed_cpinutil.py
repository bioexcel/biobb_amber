#!/usr/bin/env python3

"""Module containing the ParmedCpinUtil class and the command line interface."""
import argparse
from typing import Optional
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_amber.parmed.common import check_input_path, check_output_path


class ParmedCpinUtil(BiobbObject):
    """
    | biobb_amber ParmedCpinUtil
    | Wrapper of the `AmberTools (AMBER MD Package) parmed tool <https://ambermd.org/AmberTools.php>`_ module.
    | Creates a cpin file for constant pH simulations from an AMBER topology file using parmed tool from the AmberTools MD package.

    Args:
        input_top_path (str): Input AMBER topology file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/parmed/structure.solv.top>`_. Accepted formats: top (edam:format_3881), parmtop (edam:format_3881), prmtop (edam:format_3881).
        output_cpin_path (str): Output AMBER constant pH input (CPin) file. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/parmed/cln025.cpin>`_. Accepted formats: cpin (edam:format_2330).
        output_top_path (str) (Optional): Output topology file (AMBER ParmTop). File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/parmed/cln025.cpH.prmtop>`_. Accepted formats: top (edam:format_3881), parmtop (edam:format_3881), prmtop (edam:format_3881).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **resnames** (*str*) - ("None") Residue names to include in CPIN file. Values: AS4, GL4, HIP, CYS, LYS, TYR.
            * **igb** (*int*) - (2) Generalized Born model which you intend to use to evaluate dynamics or protonation state swaps. Values: 1, 2, 5, 7, 8.
            * **system** (*str*) - ("Unknown") Name of system to titrate.
            * **binary_path** (*str*) - ("cpinutil.py") Path to the cpinutil.py executable binary.
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

            from biobb_amber.parmed.parmed_cpinutil import parmed_cpinutil
            prop = {
                'igb' : 2,
                'resnames': 'AS4 GL4',
                'system': 'cln025',
                'remove_tmp': False
            }
            parmed_cpinutil(input_top_path='/path/to/topology.top',
                          output_cpin_path='/path/to/newCpin.cpin',
                          output_top_path='/path/to/newTopology.top',
                          properties=prop)

    Info:
        * wrapped_software:
            * name: AmberTools parmed
            * version: >20.9
            * license: LGPL 2.1
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, input_top_path, output_cpin_path, output_top_path=None, properties=None, **kwargs) -> None:

        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            'in': {'input_top_path': input_top_path},
            'out': {'output_cpin_path': output_cpin_path,
                    'output_top_path': output_top_path}
        }

        # Properties specific for BB
        self.properties = properties
        self.resnames = properties.get('resnames')
        self.igb = properties.get('igb', 2)
        self.system = properties.get('system', "Unknown")
        self.binary_path = properties.get('binary_path', 'cpinutil.py')

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    def check_data_params(self, out_log, err_log):
        """ Checks input/output paths correctness """

        # Check input(s)
        self.io_dict["in"]["input_top_path"] = check_input_path(self.io_dict["in"]["input_top_path"], "input_top_path", False, out_log, self.__class__.__name__)

        # Check output(s)
        self.io_dict["out"]["output_cpin_path"] = check_output_path(self.io_dict["out"]["output_cpin_path"], "output_cpin_path", False, out_log, self.__class__.__name__)
        self.io_dict["out"]["output_top_path"] = check_output_path(self.io_dict["out"]["output_top_path"], "output_top_path", True, out_log, self.__class__.__name__)

    @launchlogger
    def launch(self):
        """Launches the execution of the ParmedCpinUtil module."""

        # check input/output paths and parameters
        self.check_data_params(self.out_log, self.err_log)

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir()
        fu.log('Creating %s temporary folder' % self.tmp_folder, self.out_log)

        # cpinutil.py -igb 2 -resname AS4 GL4 -p $1.prmtop -op $1.cpH.prmtop
        # cpinutil.py -p cln025.cpH.prmtop -igb 2 -system "CLN" -o cpin

        fu.log('Creating command line with instructions and required arguments', self.out_log, self.global_log)

        self.cmd = [self.binary_path,
                    '-p', self.stage_io_dict['in']['input_top_path'],
                    '-o', self.stage_io_dict['out']['output_cpin_path']
                    ]

        if self.igb:
            self.cmd.append('-igb')
            self.cmd.append(str(self.igb))

        if self.system:
            self.cmd.append('-system')
            self.cmd.append(self.system)

        if self.resnames:
            self.cmd.append('-resnames')
            self.cmd.append(self.resnames)

        if self.io_dict["out"]["output_top_path"]:
            self.cmd.append('-op')
            self.cmd.append(self.stage_io_dict["out"]["output_top_path"])

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        # remove temporary folder(s)
        self.tmp_files.extend([
            self.stage_io_dict.get("unique_dir", ""),
            self.tmp_folder
        ])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def parmed_cpinutil(input_top_path: str, output_cpin_path: str,
                    output_top_path: Optional[str] = None,
                    properties: Optional[dict] = None, **kwargs) -> int:
    """Create :class:`ParmedCpinUtil <parmed.parmed_cpinutil.ParmedCpinUtil>`parmed.parmed_cpinutil.ParmedCpinUtil class and
    execute :meth:`launch() <parmed.parmed_cpinutil.ParmedCpinUtil.launch>` method"""

    return ParmedCpinUtil(input_top_path=input_top_path,
                          output_cpin_path=output_cpin_path,
                          output_top_path=output_top_path,
                          properties=properties).launch()


def main():
    parser = argparse.ArgumentParser(description='create a cpin file for constant pH simulations from an AMBER topology file using parmed program from AmberTools MD package.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_top_path', required=True, help='Input AMBER topology file. Accepted formats: top, parmtop, prmtop.')
    required_args.add_argument('--output_cpin_path', required=True, help='Output AMBER constant pH input (CPin) file. Accepted formats: cpin.')
    required_args.add_argument('--output_top_path', required=False, help='Output topology file (AMBER ParmTop). Accepted formats: top, parmtop, prmtop.')

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call
    parmed_cpinutil(input_top_path=args.input_top_path,
                    output_cpin_path=args.output_cpin_path,
                    output_top_path=args.output_top_path,
                    properties=properties)


if __name__ == '__main__':
    main()
