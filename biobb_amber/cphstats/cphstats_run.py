#!/usr/bin/env python3

"""Module containing the Cphstats class and the command line interface."""

from typing import Optional
from biobb_common.generic.biobb_object import BiobbObject, launcher

from biobb_amber.cphstats.common import stats_cmd


class CphstatsRun(BiobbObject):
    """
    | biobb_amber CphstatsRun
    | Wrapper of the `AmberTools (AMBER MD Package) cphstats tool <https://ambermd.org/AmberTools.php>`_ module.
    | Analyzing the results of constant pH MD simulations using cphstats tool from the AMBER MD package.

    Args:
        input_cpin_path (str): Input constant pH file (AMBER cpin). File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/cphstats/structure.cpin>`_. Accepted formats: cpin (edam:format_2330), in (edam:format_2330), txt (edam:format_2330).
        input_cpout_path (str): Output constant pH file (AMBER cpout). File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/cphstats/sander.pH.cpout>`_. Accepted formats: cpout (edam:format_2330), zip (edam:format_3987), gzip (edam:format_3987), gz (edam:format_3989).
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
        super().__init__(**locals())

    def run(self):
        """Launches the execution of the CphstatsRun module."""

        # Command line
        # cphstats -i 4LYT.equil.cpin 0/4LYT.md1.cpout -o pH0_calcpka.dat --population pH0_populations.dat
        self.cmd = stats_cmd(self, 'input_cpin_path', 'input_cpout_path')
        self.cmd.append('-p' if self.protonated else '-d')
        if self.pka:
            self.cmd.append('-a')
        self.cmd.append('--calcpka' if self.calcpka else '--no-calcpka')

        self.run_biobb()


cphstats_run = launcher(CphstatsRun)

if __name__ == '__main__':
    CphstatsRun.main()
