#!/usr/bin/env python3

"""Module containing the NabBuildDNAStructure class and the command line interface."""
import argparse
import shutil
from pathlib import Path, PurePath
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_amber.nab.common import *

class NabBuildDNAStructure(BiobbObject):
    """
    | biobb_amber.nab.nab_build_dna_structure NabBuildDNAStructure
    | Wrapper of the `AmberTools (AMBER MD Package) nab tool <https://ambermd.org/AmberTools.php>`_ module.
    | Builds a 3D structure from a DNA sequence using nab (Nucleic Acid Builder) tool from the AmberTools MD package.

    Args:
        output_pdb_path (str): DNA 3D structure PDB file. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/nab/ref_nab_build_dna_structure.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **sequence** (*str*) - ("GCGCGGCTGATAAACGAAAGC") Nucleotide sequence to convert to a 3D structure. Nucleotides should be written in 1-letter code, with no spaces between them.
            * **helix_type** (*str*) - ("lbdna") DNA/RNA helix type. Values: arna (Right Handed A-RNA - Arnott), aprna (Right Handed A’-RNA - Arnott), lbdna (Right Handed B-DNA - Langridge), abdna (Right Handed B-DNA - Arnott), sbdna (Left Handed B-DNA - Sasisekharan), adna (Right Handed A-DNA - Arnott).
            * **compiler** (*str*) - ("gcc") Alternative C compiler for nab.
            * **linker** (*str*) - ("gfortran") Alternative Fortran linker for nab.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_amber.nab.nab_build_dna_structure import nab_build_dna_structure
            prop = {
                'sequence': 'GCGCGGCTGATAAACGAAAGC'
            }
            nab_build_dna_structure(output_pdb_path='/path/to/newStructure.pdb',
                                    properties=prop)

    Info:
        * wrapped_software:
            * name: AmberTools nab
            * version: >20.9
            * license: LGPL 2.1
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, output_pdb_path, properties, **kwargs):

        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)

        # Input/Output files
        self.io_dict = {
            'out': { 'output_pdb_path': output_pdb_path }
        }

        # Properties specific for BB
        self.properties = properties
        self.sequence = properties.get('sequence', "GCGCGGCTGATAAACGAAAGC")
        self.helix_type = properties.get('helix_type', "lbdna")
        self.compiler = properties.get('compiler', "gcc")
        self.linker = properties.get('linker', "gfortran")

        # Check the properties
        self.check_properties(properties)

    def check_data_params(self, out_log, err_log):
        """ Checks input/output paths correctness """

        # Check output(s)
        self.io_dict["out"]["output_pdb_path"] = check_output_path(self.io_dict["out"]["output_pdb_path"],"output_pdb_path", False, out_log, self.__class__.__name__)

    @launchlogger
    def launch(self):
        """Launches the execution of the NabBuildDNAStructure module."""

        # check input/output paths and parameters
        self.check_data_params(self.out_log, self.err_log)

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir()
        fu.log('Creating %s temporary folder' % self.tmp_folder, self.out_log)

        # create .nab file
        # molecule m;
        # m = fd_helix( "abdna", "aaaaaaaaaa", "dna" );
        # putpdb( "nuc.pdb", m, "-wwpdb");

        acid_type = 'dna'
        if ("rna" in self.helix_type):
            acid_type = 'rna'

        instructions_file = str(PurePath(self.tmp_folder).joinpath("nuc.nab"))
        with open(instructions_file, 'w') as nabin:
                nabin.write("molecule m; \n")
                nabin.write("m = fd_helix( \"" + self.helix_type + "\", \"" + self.sequence + "\", \"" + acid_type + "\" ); \n")
                nabin.write("putpdb( \"" + self.io_dict['out']['output_pdb_path'] + "\" , m, \"-wwpdb\");\n")

        # Command line
        self.cmd = ['nab ',
               '--compiler', self.compiler,
               '--linker', self.linker,
               instructions_file,
               ' ; ./' + self.tmp_folder +'/nuc'
               ]

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        # remove temporary folder(s)
        if self.remove_tmp:
            self.tmp_files.append(self.tmp_folder)
            self.tmp_files.append("nab.log")
            self.tmp_files.append("tleap.out")
            self.remove_tmp_files()

        return self.return_code

def nab_build_dna_structure(output_pdb_path: str,
           properties: dict = None, **kwargs) -> int:
    """Create :class:`NabBuildDNAStructure <nab.nab_build_dna_structure.NabBuildDNAStructure>`nab.nab_build_dna_structure.NabBuildDNAStructure class and
    execute :meth:`launch() <nab.nab_build_dna_structure.NabBuildDNAStructure.launch>` method"""

    return NabBuildDNAStructure( output_pdb_path=output_pdb_path,
                        properties=properties).launch()

def main():
    parser = argparse.ArgumentParser(description='Building a 3D structure from a DNA sequence using nab.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--output_pdb_path', required=True, help='Linear (unfolded) 3D structure PDB file. Accepted formats: pdb.')

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call
    nab_build_dna_structure(output_pdb_path=args.output_pdb_path,
             properties=properties)

if __name__ == '__main__':
    main()
