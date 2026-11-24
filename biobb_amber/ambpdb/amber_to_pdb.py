#!/usr/bin/env python3

"""Module containing the AmberToPDB class and the command line interface."""

from typing import Optional
from biobb_common.generic.biobb_object import BiobbObject


class AmberToPDB(BiobbObject):
    """
    | biobb_amber AmberToPDB
    | Wrapper of the `AmberTools (AMBER MD Package) ambpdb tool <https://ambermd.org/AmberTools.php>`_ module.
    | Generates a PDB structure from AMBER topology (parmtop) and coordinates (crd) files, using the ambpdb tool from the AmberTools MD package

    Args:
        input_top_path (str): AMBER topology file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/ambpdb/structure.leap.top>`_. Accepted formats: top (edam:format_3881), parmtop (edam:format_3881), prmtop (edam:format_3881).
        input_crd_path (str): AMBER coordinates file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/ambpdb/structure.leap.crd>`_. Accepted formats: crd (edam:format_3878), mdcrd (edam:format_3878), inpcrd (edam:format_3878), rst (edam:format_3886), rst7 (edam:format_3886).
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

    def run(self):
        # Command line
        self.cmd = [self.binary_path,
                    '-p', self.stage_io_dict['in']['input_top_path'],
                    '-c', self.stage_io_dict['in']['input_crd_path'],
                    '> ', self.stage_io_dict['out']['output_pdb_path']
                    ]

        self.run_biobb()
        self.copy_to_host()
        self.remove_tmp_files()
        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def amber_to_pdb(input_top_path: str, input_crd_path: str, output_pdb_path: str,
                 properties: Optional[dict] = None, **kwargs) -> int:
    """Create the :class:`AmberToPDB <amber.amber_to_pdb.AmberToPDB>` class and
    execute the :meth:`launch() <amber.amber_to_pdb.AmberToPDB.launch>` method."""
    return AmberToPDB(**dict(locals())).launch()


amber_to_pdb.__doc__ = AmberToPDB.__doc__
main = AmberToPDB.get_main(amber_to_pdb, "Generates a PDB structure from AMBER topology (parmtop) and coordinates (crd) files, using the ambpdb tool from the AmberTools MD package.")

if __name__ == '__main__':
    main()
