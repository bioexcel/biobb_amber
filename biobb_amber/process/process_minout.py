#!/usr/bin/env python3

"""Module containing the ProcessMinOut class and the command line interface."""

import argparse
import shutil
from pathlib import Path, PurePath
from typing import Optional

from biobb_common.configuration import settings
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger

from biobb_amber.process.common import (
    _from_string_to_list,
    check_input_path,
    check_output_path,
)


class ProcessMinOut(BiobbObject):
    """
    | biobb_amber.process.process_minout ProcessMinOut
    | Wrapper of the `AmberTools (AMBER MD Package) process_minout tool <https://ambermd.org/AmberTools.php>`_ module.
    | Parses the AMBER (sander) minimization output file (log) and dumps statistics that can then be plotted. Using the process_minout.pl tool from the AmberTools MD package.

    Args:
        input_log_path (str): AMBER (sander) Minimization output (log) file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/process/sander.min.log>`_. Accepted formats: log (edam:format_2330), out (edam:format_2330), txt (edam:format_2330), o (edam:format_2330).
        output_dat_path (str): Dat output file containing data from the specified terms along the minimization process. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/process/sander.min.energy.dat>`_. Accepted formats: dat (edam:format_1637), txt (edam:format_2330), csv (edam:format_3752).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **terms** (*list*) - (["ENERGY"]) Statistics descriptors. Values: ANGLE, BOND, DIHEDRAL, EEL, EEL14, ENERGY, GMAX, HBOND, NAME, NSTEP, NUMBER, RESTRAINT, RMS, VDW14, VDWAALS.
            * **binary_path** (*str*) - ("process_minout.perl") Path to the process_minout.perl executable binary.
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

            from biobb_amber.process.process_minout import process_minout
            prop = {
                'terms' : ['ENERGY','RMS']
            }
            process_minout(input_log_path='/path/to/ambermin.log',
                          output_dat_path='/path/to/newFeature.dat',
                          properties=prop)

    Info:
        * wrapped_software:
            * name: AmberTools process_minout
            * version: >20.9
            * license: LGPL 2.1
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, input_log_path: str, output_dat_path: str, properties, **kwargs):
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            "in": {"input_log_path": input_log_path},
            "out": {"output_dat_path": output_dat_path},
        }

        # Properties specific for BB
        self.properties = properties
        self.terms = _from_string_to_list(properties.get("terms", ["ENERGY"]))
        self.binary_path = properties.get("binary_path", "process_minout.perl")

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    def check_data_params(self, out_log, out_err):
        """Checks input/output paths correctness"""

        # Check input(s)
        self.io_dict["in"]["input_log_path"] = check_input_path(
            self.io_dict["in"]["input_log_path"],
            "input_log_path",
            False,
            out_log,
            self.__class__.__name__,
        )

        # Check output(s)
        self.io_dict["out"]["output_dat_path"] = check_output_path(
            self.io_dict["out"]["output_dat_path"],
            "output_dat_path",
            False,
            out_log,
            self.__class__.__name__,
        )

    @launchlogger
    def launch(self):
        """Launches the execution of the ProcessMinOut module."""

        # check input/output paths and parameters
        self.check_data_params(self.out_log, self.err_log)

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        if not self.container_path:
            self.tmp_folder = fu.create_unique_dir()
            fu.log("Creating %s temporary folder" % self.tmp_folder, self.out_log)
            self.cmd = [
                "cd",
                self.tmp_folder,
                ";",
                self.binary_path,
                str(Path(self.stage_io_dict["in"]["input_log_path"]).resolve()),
            ]
        else:
            self.tmp_folder = None
            self.cmd = [self.binary_path, self.stage_io_dict["in"]["input_log_path"]]

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        if len(self.terms) == 1:
            if self.container_path:
                shutil.copy(
                    PurePath(self.stage_io_dict["unique_dir"]).joinpath(
                        "summary." + self.terms[0]
                    ),
                    self.io_dict["out"]["output_dat_path"],
                )
            else:
                shutil.copy(
                    PurePath(str(self.tmp_folder)).joinpath("summary." + self.terms[0]),
                    self.io_dict["out"]["output_dat_path"],
                )
        else:
            if self.container_path:
                tmp = self.stage_io_dict["unique_dir"]
            else:
                tmp = self.tmp_folder

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

            with open(self.io_dict["out"]["output_dat_path"], "w") as fp_out:
                fp_out.write("# TIME ")
                for term in self.terms:
                    fp_out.write(term + " ")
                fp_out.write("\n")
                for key in sorted(ene_dict.keys()):
                    fp_out.write(str(key) + " ")
                    for term in self.terms:
                        fp_out.write(ene_dict[key][term] + " ")
                    fp_out.write("\n")

        # remove temporary folder(s)
        self.tmp_files.extend(
            [self.stage_io_dict.get("unique_dir", ""), str(self.tmp_folder)] + list(Path().glob("summary*"))
        )
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def process_minout(
    input_log_path: str,
    output_dat_path: str,
    properties: Optional[dict] = None,
    **kwargs,
) -> int:
    """Create :class:`ProcessMinOut <process.process_mdout.ProcessMinOut>`process.process_mdout.ProcessMinOut class and
    execute :meth:`launch() <process.process_mdout.ProcessMinOut.launch>` method"""

    return ProcessMinOut(
        input_log_path=input_log_path,
        output_dat_path=output_dat_path,
        properties=properties,
    ).launch()


def main():
    parser = argparse.ArgumentParser(
        description="Parses the AMBER (sander) minimization output file (log) and dumps statistics that can then be plotted. Using the process_minout.pl tool from the AmberTools MD package.",
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999),
    )
    parser.add_argument("--config", required=False, help="Configuration file")

    # Specific args
    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument(
        "--input_log_path",
        required=True,
        help="AMBER (sander) minimization output (log) file. Accepted formats: log, out, txt, o.",
    )
    required_args.add_argument(
        "--output_dat_path",
        required=True,
        help="Dat output file containing data from the specified terms along the minimization process. File type: output. Accepted formats: dat, txt, csv.",
    )

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call
    process_minout(
        input_log_path=args.input_log_path,
        output_dat_path=args.output_dat_path,
        properties=properties,
    )


if __name__ == "__main__":
    main()
