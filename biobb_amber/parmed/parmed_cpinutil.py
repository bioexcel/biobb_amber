#!/usr/bin/env python3

"""Module containing the ParmedCpinUtil class and the command line interface."""

from typing import Optional
from biobb_common.generic.biobb_object import BiobbObject, launcher
from biobb_common.tools import file_utils as fu


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
            * **resnames** (*str*) - (None) Residue names to include in CPIN file. Values: AS4, GL4, HIP, CYS, LYS, TYR.
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

    def __init__(self, input_top_path: str, output_cpin_path: str, output_top_path: Optional[str] = None, properties: Optional[dict] = None, **kwargs) -> None:
        super().__init__(**locals())

    def run(self):
        """Launches the execution of the ParmedCpinUtil module."""

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


parmed_cpinutil = launcher(ParmedCpinUtil)

if __name__ == '__main__':
    ParmedCpinUtil.main()
