#!/usr/bin/env python3

"""Module containing the Cphstats class and the command line interface."""
import argparse
from typing import Optional
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools.file_utils import launchlogger
from biobb_amber.cphstats.common import check_input_path, check_output_path


class CphstatsRun(BiobbObject):
    """
    | biobb_amber CphstatsRun
    | Wrapper of the `AmberTools (AMBER MD Package) cphstats tool <https://ambermd.org/AmberTools.php>`_ module.
    | Analyzing the results of constant pH MD simulations using cphstats tool from the AMBER MD package.

    Args:
        input_cpin_path (str): Input constant pH file (AMBER cpin). File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/cphstats/structure.cpin>`_. Accepted formats: cpin (edam:format_2330).
        input_cpout_path (str): Output constant pH file (AMBER cpout). File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/cphstats/sander.pH.cpout>`_. Accepted formats: cpout (edam:format_2330), zip (edam:format_3987), gzip (edam:format_3987).
        output_dat_path (str): Output file to which the standard calcpka-type statistics are written. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/cphstats/cphstats.pH.dat>`_. Accepted formats: dat (edam:format_2330), out (edam:format_2330), txt (edam:format_2330), o (edam:format_2330).
        output_population_path (str) (Optional): Output file where protonation state populations are printed for every state of every residue. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/cphstats/cphstats.pH.pop.dat>`_. Accepted formats: dat (edam:format_2330), out (edam:format_2330), txt (edam:format_2330), o (edam:format_2330).
        output_chunk_path (str) (Optional): Output file where the time series data calculated over chunks of the simulation are printed. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/cphstats/cphstats.pH.dat>`_. Accepted formats: dat (edam:format_2330), out (edam:format_2330), txt (edam:format_2330), o (edam:format_2330).
        output_cumulative_path (str) (Optional): Output file where the cumulative time series data is printed. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/cphstats/cphstats.pH.dat>`_. Accepted formats: dat (edam:format_2330), out (edam:format_2330), txt (edam:format_2330), o (edam:format_2330).
        output_conditional_path (str) (Optional): Output file with requested conditional probabilities. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/cphstats/cphstats.pH.dat>`_. Accepted formats: dat (edam:format_2330), out (edam:format_2330), txt (edam:format_2330), o (edam:format_2330).
        output_chunk_conditional_path (str) (Optional): Output file with a time series of the conditional probabilities over a trajectory split up into chunks. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/cphstats/cphstats.pH.dat>`_. Accepted formats: dat (edam:format_2330), out (edam:format_2330), txt (edam:format_2330), o (edam:format_2330).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **timestep** (*float*) - (0.002) Simulation time step -in ps-, used to print data as a function of time.
            * **verbose** (*bool*) - (False) Controls how much information is printed to the calcpka-style output file. Options are: False - Just print fraction protonated. True - Print everything calcpka prints.
            * **interval** (*int*) - (1000) Interval between which to print out time series data like chunks, cumulative data, and running averages. It is also used as the window of the conditional probability time series.
            * **protonated** (*bool*) - (True) Print out protonation fraction instead of deprotonation fraction in time series data.
            * **pka** (*bool*) - (False) Print predicted pKas -via Henderson-Hasselbalch equation- in place of fraction -de-protonated.
            * **calcpka** (*bool*) - (True) Triggers the calcpka-style output.
            * **running_avg_window** (*int*) - (100) Defines a window size -in MD steps- for a moving, running average time series.
            * **chunk_window** (*int*) - (100) Computes the time series data over a chunk of the simulation of this specified size -window- time steps.
            * **cumulative** (*bool*) - (False) Computes the cumulative average time series data over the course of the trajectory.
            * **fix_remd** (*str*) - ("") This option will trigger cphstats to reassemble the titration data into pH-specific ensembles. This is an exclusive mode of the program, no other analyses will be done.
            * **conditional** (*str*) - ("") Evaluates conditional probabilities. CONDITIONAL should be a string of the format: <resid>:<state>,<resid>:<state>,... or <resid>:PROT,<resid>:DEPROT,... or <resid>:<state1>;<state2>,<resid>:PROT,... where <resid> is the residue number in the prmtop and <state> is either the state number or -p-rotonated or -d-eprotonated, case-insensitive.
            * **binary_path** (*str*) - ("cphstats") Path to the cphstats executable binary.
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

            from biobb_amber.cphstats.cphstats_run import cphstats_run
            prop = {
                'timestep' : 0.002
            }
            cphstats_run(input_cpin_path='/path/to/cpin.cpin',
                         input_cpout_path='/path/to/cpout.cpout',
                         output_dat_path='/path/to/cphstats.dat',
                         properties=prop)

    Info:
        * wrapped_software:
            * name: AMBER cphstats
            * version: >=1.5
            * license: other
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, input_cpin_path: str, input_cpout_path: str, output_dat_path: str, output_population_path: Optional[str] = None,
                 output_chunk_path: Optional[str] = None, output_cumulative_path: Optional[str] = None, output_conditional_path: Optional[str] = None, output_chunk_conditional_path: Optional[str] = None,
                 properties: Optional[dict] = None, **kwargs) -> None:

        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            'in': {'input_cpin_path': input_cpin_path,
                   'input_cpout_path': input_cpout_path},
            'out': {'output_dat_path': output_dat_path,
                    'output_population_path': output_population_path,
                    'output_chunk_path': output_chunk_path,
                    'output_cumulative_path': output_cumulative_path,
                    'output_conditional_path': output_conditional_path,
                    'output_chunk_conditional_path': output_chunk_conditional_path}
        }

        # Properties specific for BB
        self.properties = properties
        self.timestep = properties.get('timestep', 0.002)
        self.verbose = properties.get('verbose', False)
        self.interval = properties.get('interval', 1000)
        self.protonated = properties.get('protonated', True)
        self.pka = properties.get('pka', False)
        self.calcpka = properties.get('calcpka', True)
        self.running_avg_window = properties.get('running_avg_window', 100)
        self.chunk_window = properties.get('chunk_window', 100)
        self.cumulative = properties.get('cumulative', False)
        self.fix_remd = properties.get('fix_remd', "")
        self.conditional = properties.get('conditional', "")
        self.binary_path = properties.get('binary_path', 'cphstats')

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    def check_data_params(self, out_log, err_log):
        """ Checks input/output paths correctness """

        # Check input(s)
        self.io_dict["in"]["input_cpin_path"] = check_input_path(self.io_dict["in"]["input_cpin_path"], "input_cpin_path", False, out_log, self.__class__.__name__)
        self.io_dict["in"]["input_cpout_path"] = check_input_path(self.io_dict["in"]["input_cpout_path"], "input_cpout_path", False, out_log, self.__class__.__name__)

        # Check output(s)
        self.io_dict["out"]["output_dat_path"] = check_output_path(self.io_dict["out"]["output_dat_path"], "output_dat_path", False, out_log, self.__class__.__name__)
        self.io_dict["out"]["output_population_path"] = check_output_path(self.io_dict["out"]["output_population_path"], "output_population_path", True, out_log, self.__class__.__name__)
        self.io_dict["out"]["output_chunk_path"] = check_output_path(self.io_dict["out"]["output_chunk_path"], "output_chunk_path", True, out_log, self.__class__.__name__)
        self.io_dict["out"]["output_cumulative_path"] = check_output_path(self.io_dict["out"]["output_cumulative_path"], "output_cumulative_path", True, out_log, self.__class__.__name__)
        self.io_dict["out"]["output_chunk_conditional_path"] = check_output_path(self.io_dict["out"]["output_chunk_conditional_path"], "output_chunk_conditional_path", True, out_log, self.__class__.__name__)
        self.io_dict["out"]["output_conditional_path"] = check_output_path(self.io_dict["out"]["output_conditional_path"], "output_conditional_path", True, out_log, self.__class__.__name__)

    @launchlogger
    def launch(self):
        """Launches the execution of the CphstatsRun module."""

        # check input/output paths and parameters
        self.check_data_params(self.out_log, self.err_log)

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # Command line
        # cphstats -i 4LYT.equil.cpin 0/4LYT.md1.cpout -o pH0_calcpka.dat --population pH0_populations.dat
        self.cmd = [self.binary_path,
                    '-O',
                    '-i', self.stage_io_dict['in']['input_cpin_path'],
                    '-o', self.stage_io_dict['out']['output_dat_path'],
                    self.stage_io_dict['in']['input_cpout_path']
                    ]

        if self.io_dict['out']['output_population_path']:
            self.cmd.append('--population ')
            self.cmd.append(self.stage_io_dict['out']['output_population_path'])

        if self.io_dict['out']['output_chunk_path']:
            self.cmd.append('--chunk-out ')
            self.cmd.append(self.stage_io_dict['out']['output_chunk_path'])
            if self.chunk_window:
                self.cmd.append('--chunk')
                self.cmd.append(str(self.chunk_window))

        if self.io_dict['out']['output_cumulative_path']:
            self.cmd.append('--cumulative-out ')
            self.cmd.append(self.stage_io_dict['out']['output_cumulative_path'])

        if self.io_dict['out']['output_conditional_path']:
            self.cmd.append('--conditional-output ')
            self.cmd.append(self.stage_io_dict['out']['output_conditional_path'])

        if self.io_dict['out']['output_chunk_conditional_path']:
            self.cmd.append('--chunk-conditional ')
            self.cmd.append(self.stage_io_dict['out']['output_chunk_conditional_path'])

        if self.verbose:
            self.cmd.append('-v 1')

        if self.interval:
            self.cmd.append('-n')
            self.cmd.append(str(self.interval))

        if self.protonated:
            self.cmd.append('-p')
        else:
            self.cmd.append('-d')

        if self.pka:
            self.cmd.append('-a')

        if self.calcpka:
            self.cmd.append('--calcpka')
        else:
            self.cmd.append('--no-calcpka')

        if self.running_avg_window:
            self.cmd.append('-r')
            self.cmd.append(str(self.running_avg_window))

        if self.cumulative:
            self.cmd.append('--cumulative')

        if self.fix_remd:
            self.cmd.append('--fix-remd')
            self.cmd.append(str(self.fix_remd))

        if self.conditional:
            self.cmd.append('-c')
            self.cmd.append(str(self.conditional))

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        # Remove temporary file(s)
        self.tmp_files.extend([
            self.stage_io_dict.get("unique_dir", "")
        ])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def cphstats_run(input_cpin_path: str, input_cpout_path: str,
                 output_dat_path: str,
                 output_population_path: Optional[str] = None, output_chunk_path: Optional[str] = None,
                 output_conditional_path: Optional[str] = None, output_chunk_conditional_path: Optional[str] = None,
                 output_cumulative_path: Optional[str] = None,
                 properties: Optional[dict] = None, **kwargs) -> int:
    """Create :class:`CphstatsRun <cphstats.chpstats_run.CphstatsRun>`cphstats.chpstats_run.CphstatsRun class and
    execute :meth:`launch() <cphstats.chpstats_run.CphstatsRun.launch>` method"""

    return CphstatsRun(input_cpin_path=input_cpin_path,
                       input_cpout_path=input_cpout_path,
                       output_dat_path=output_dat_path,
                       output_population_path=output_population_path,
                       output_chunk_path=output_chunk_path,
                       output_chunk_conditional_path=output_chunk_conditional_path,
                       output_conditional_path=output_conditional_path,
                       output_cumulative_path=output_cumulative_path,
                       properties=properties).launch()


def main():
    parser = argparse.ArgumentParser(description='Analyzing the results of constant pH MD simulations using cphstats tool from the AMBER MD package.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_cpin_path', required=True, help='Input constant pH file (AMBER cpin). Accepted formats: cpin.')
    required_args.add_argument('--input_cpout_path', required=True, help='Output constant pH file (AMBER cpout). Accepted formats: cpout.')
    required_args.add_argument('--output_dat_path', required=True, help='Output file to which the standard calcpka-type statistics are written. Accepted formats: dat, out, txt, o.')
    required_args.add_argument('--output_population_path', required=False, help='Output file where protonation state populations are printed for every state of every residue. Accepted formats: dat, out, txt, o.')
    required_args.add_argument('--output_chunk_path', required=False, help='Output file where the time series data calculated over chunks of the simulation are printed. Accepted formats: dat, out, txt, o.')
    required_args.add_argument('--output_cumulative_path', required=False, help='Output file where the cumulative time series data is printed. Accepted formats: dat, out, txt, o.')
    required_args.add_argument('--output_conditional_path', required=False, help='Output file with requested conditional probabilities. Accepted formats: dat, out, txt, o.')
    required_args.add_argument('--output_chunk_conditional_path', required=False, help='Output file with a time series of the conditional probabilities over a trajectory split up into chunks. Accepted formats: dat, out, txt, o.')

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call
    cphstats_run(input_cpin_path=args.input_cpin_path,
                 input_cpout_path=args.input_cpout_path,
                 output_dat_path=args.output_dat_path,
                 output_population_path=args.output_population_path,
                 output_chunk_path=args.output_chunk_path,
                 output_cumulative_path=args.output_cumulative_path,
                 output_conditional_path=args.output_conditional_path,
                 output_chunk_conditional_path=args.output_chunk_conditional_path,
                 properties=properties)


if __name__ == '__main__':
    main()
