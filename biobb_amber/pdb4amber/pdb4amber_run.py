#!/usr/bin/env python3

"""Module containing the Pdb4amber class and the command line interface."""
from typing import Optional
from biobb_common.generic.biobb_object import BiobbObject, launcher


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

    def __init__(self, input_pdb_path: str, output_pdb_path: str, properties: Optional[dict] = None, **kwargs):
        super().__init__(**locals())

    def run(self):
        """Launches the execution of the Pdb4amberRun module."""

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


pdb4amber_run = launcher(Pdb4amberRun)

if __name__ == '__main__':
    Pdb4amberRun.main()
