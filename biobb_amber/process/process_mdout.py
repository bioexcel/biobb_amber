#!/usr/bin/env python3

"""Module containing the ProcessMDOut class and the command line interface."""

import shutil
# import os
from pathlib import Path, PurePath
from typing import Optional

from biobb_common.generic.biobb_object import BiobbObject, launcher
from biobb_common.tools import file_utils as fu

from biobb_amber.process.common import (
    _from_string_to_list,
)


class ProcessMDOut(BiobbObject):
    """
    | biobb_amber.process.process_mdout ProcessMDOut
    | Wrapper of the `AmberTools (AMBER MD Package) process_mdout tool <https://ambermd.org/AmberTools.php>`_ module.
    | Parses the AMBER (sander) md output file (log) and dumps statistics that can then be plotted. Using the process_mdout.pl tool from the AmberTools MD package.

    Args:
        input_log_path (str): AMBER (sander) MD output (log) file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/process/sander.heat.log>`_. Accepted formats: log (edam:format_2330), out (edam:format_2330), txt (edam:format_2330), o (edam:format_2330).
        output_dat_path (str): Dat output file containing data from the specified terms along the minimization process. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/process/sander.md.temp.dat>`_. Accepted formats: dat (edam:format_1637), txt (edam:format_2330), csv (edam:format_3752).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **terms** (*list*) - (["ETOT"]) Statistics descriptors. Values: VOLUME, TSOLVENT, TSOLUTE, TEMP, PRES, ETOT, ESCF, EPTOT, EKTOT, EKCMT, DENSITY.
            * **binary_path** (*str*) - ("process_mdout.perl") Path to the process_mdout.perl executable binary.
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

            from biobb_amber.process.process_mdout import process_mdout
            prop = {
                'terms' : ['TEMP','VOLUME','DENSITY']
            }
            process_mdout(input_log_path='/path/to/ambermd.log',
                          output_dat_path='/path/to/newFeature.dat',
                          properties=prop)

    Info:
        * wrapped_software:
            * name: AmberTools process_mdout
            * version: >20.9
            * license: LGPL 2.1
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, input_log_path: str, output_dat_path: str, properties: Optional[dict] = None, **kwargs):
        super().__init__(**locals())

        # Properties specific for BB
        self.terms = _from_string_to_list(self.terms)

    def run(self):
        """Launches the execution of the ProcessMDOut module."""

        # is_docker = self.container_path and os.path.basename(str(self.container_path)).lower() == 'docker'

        if not self.container_path:
            # No container or Singularity: cd to tmp_folder so summary.* files land there
            tmp_folder = self.create_tmp_dir(log=True)
            self.cmd = [
                "cd",
                tmp_folder,
                ";",
                self.binary_path,
                str(Path(self.stage_io_dict["in"]["input_log_path"]).resolve()),
            ]
        else:
            # Docker: working dir is handled via container_working_dir
            tmp_folder = None
            self.cmd = [self.binary_path, self.stage_io_dict["in"]["input_log_path"]]

        if self.container_path:
            if not self.container_working_dir:
                fu.log('WARNING: container_working_dir property was not set. Defining it with the same value as container_volume_path', self.out_log, self.global_log)
                self.container_working_dir = self.container_volume_path

        # Run Biobb block
        self.run_biobb()

        # Write the output dat file from the summary.<term> files written by process_mdout.perl.
        if len(self.terms) == 1:
            if self.container_path:
                shutil.copy(
                    PurePath(self.stage_io_dict["unique_dir"]).joinpath(
                        "summary." + self.terms[0]
                    ),
                    self.sandbox_file("output_dat_path"),
                )
            else:
                shutil.copy(
                    PurePath(str(tmp_folder)).joinpath("summary." + self.terms[0]),
                    self.sandbox_file("output_dat_path"),
                )
        else:
            if self.container_path:
                tmp = self.stage_io_dict["unique_dir"]
            else:
                tmp = tmp_folder

            ene_dict = {}
            for term in self.terms:
                with open(str(tmp) + "/summary." + term) as fp:
                    for line in fp:
                        x = line.split()
                        if x:
                            if len(x) > 1:
                                ene_dict.setdefault(float(x[0]), {})[term] = x[1]
                            else:
                                ene_dict.setdefault(float(x[0]), {})[term] = "-"

            with open(self.sandbox_file("output_dat_path"), "w") as fp_out:
                fp_out.write("# TIME ")
                for term in self.terms:
                    fp_out.write(term + " ")
                fp_out.write("\n")
                for key in sorted(ene_dict.keys()):
                    fp_out.write(str(key) + " ")
                    for term in self.terms:
                        fp_out.write(ene_dict[key][term] + " ")
                    fp_out.write("\n")


process_mdout = launcher(ProcessMDOut)

if __name__ == "__main__":
    ProcessMDOut.main()
