#!/usr/bin/env python3

"""Module containing the ParmedHMassRepartition class and the command line interface."""
from typing import Optional
from pathlib import PurePath
from biobb_common.generic.biobb_object import BiobbObject, launcher


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

    def __init__(self, input_top_path: str, output_top_path: Optional[str], properties: Optional[dict] = None, **kwargs) -> None:
        super().__init__(**locals())

    def run(self):
        """Launches the execution of the ParmedHMassRepartition module."""

        # Temporary folder in the sandbox & Parmed configuration (instructions) file
        instructions_file = str(PurePath(self.create_tmp_dir()).joinpath("parmed.in"))
        instructions_file_path = self.staged_path(instructions_file)

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


parmed_hmassrepartition = launcher(ParmedHMassRepartition)

if __name__ == '__main__':
    ParmedHMassRepartition.main()
