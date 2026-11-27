"""Common functions for the sander and pmemd blocks"""

import re
import shutil
from typing import Any, Dict, Optional


def write_mdin(path: str, input_mdin_path: Optional[str], mdin: Dict[str, Any], simulation_type: str, direct_mdin: bool = False) -> str:
    """Go from an input mdin file and/or the mdin and simulation_type properties to the mdin file
    written in **path** (sander format, also read by pmemd); with **direct_mdin**, a copy of the input mdin."""
    mdin = {k: str(v) for k, v in mdin.items()}
    # Amber masks are strings of the &cntrl namelist: quoted
    if mdin.get('restraintmask') and mdin['restraintmask'][0] != '"' and mdin['restraintmask'][-1] != '"':
        mdin['restraintmask'] = "\"" + mdin['restraintmask'] + "\""

    mdin_list = []
    mdin_firstPart = []
    mdin_middlePart = []
    mdin_lastPart = []

    if input_mdin_path:
        # MDIN parameters read from an input mdin file
        if (not direct_mdin):
            mdin_firstPart.append("Mdin read from input file: " + input_mdin_path)
            mdin_firstPart.append("and modified by the biobb_amber module from the BioBB library ")
            with open(input_mdin_path) as input_params:
                firstPart = True
                secondPart = False
                for line in input_params:
                    if '=' in line and not secondPart:
                        firstPart = False
                        mdin_middlePart.append(line.rstrip())
                    else:
                        if (firstPart):
                            mdin_firstPart.append(line.rstrip())
                        elif (secondPart):
                            mdin_lastPart.append(line.rstrip())
                        else:
                            secondPart = True
                            mdin_lastPart.append(line.rstrip())

            for line in mdin_middlePart:
                if ('!' in line or '#' in line) and not ('!@' in line or '!:' in line):
                    # Parsing lines with comments (#,!), e.g. :
                    # ntc=2, ntf=2, ! SHAKE, constrain lenghts of the bonds having H
                    params = re.split('!|#', line)
                    for param in params[0].split(','):
                        if param.strip():
                            mdin_list.append("  " + param.strip() + " ! " + params[1])
                elif ('@' in line or ':' in line):
                    # Parsing masks, e.g. :
                    # restraintmask = ":1-40@P,O5',C5',C4',C3',O3'", restraint_wt = 0.5
                    mylist = re.findall(r'(?:[^,"]|"(?:\\.|[^"])*")+', line)
                    [mdin_list.append("  " + i.lstrip()) for i in mylist]  # type: ignore
                else:
                    for param in line.split(','):
                        if param.strip():
                            if not param.strip().startswith('!'):
                                mdin_list.append("  " + param.strip())

    else:
        # MDIN parameters added by the biobb_amber module
        mdin_list.append("This mdin file has been created by the biobb_amber module from the BioBB library ")

        sim_type = simulation_type.lower()  # the docs list NVT, the workflows pass nvt
        minimization = (sim_type == 'minimization')
        min_vacuo = (sim_type == 'min_vacuo')
        heat = (sim_type == 'heat')
        nvt = (sim_type == 'nvt')
        npt = (sim_type == 'npt')
        free = (sim_type == 'free')
        md = (nvt or npt or free or heat)

        mdin_list.append("Type of mdin: " + sim_type)
        mdin_list.append("&cntrl")

        # Pre-configured simulation type parameters
        if minimization:
            mdin_list.append("  imin = 1 ! BioBB simulation_type minimization")
        if min_vacuo:
            mdin_list.append("  imin = 1 ! BioBB simulation_type min_vacuo")
            mdin_list.append("  ncyc = 250 ! BioBB simulation_type min_vacuo")
            mdin_list.append("  ntb = 0 ! BioBB simulation_type min_vacuo")
            mdin_list.append("  igb = 0 ! BioBB simulation_type min_vacuo")
            mdin_list.append("  cut = 12 ! BioBB simulation_type min_vacuo")
        if md:
            mdin_list.append("  imin = 0 ! BioBB simulation_type nvt|npt|free|heat")
            mdin_list.append("  cut = 10.0 ! BioBB simulation_type nvt|npt|free|heat")
            mdin_list.append("  ntr = 0 ! BioBB simulation_type nvt|npt|free|heat")
            mdin_list.append("  ntc = 2 ! BioBB simulation_type nvt|npt|free|heat")
            mdin_list.append("  ntf = 2 ! BioBB simulation_type nvt|npt|free|heat")
            mdin_list.append("  ntt = 3 ! BioBB simulation_type nvt|npt|free|heat")
            mdin_list.append("  ig = -1 ! BioBB simulation_type nvt|npt|free|heat")
            mdin_list.append("  ioutfm = 1 ! BioBB simulation_type nvt|npt|free|heat")
            mdin_list.append("  iwrap = 1 ! BioBB simulation_type nvt|npt|free|heat")
            mdin_list.append("  nstlim = 5000 ! BioBB simulation_type nvt|npt|free|heat")
            mdin_list.append("  dt = 0.002 ! BioBB simulation_type nvt|npt|free|heat")
        if npt:
            mdin_list.append("  irest = 1 ! BioBB simulation_type npt")
            mdin_list.append("  gamma_ln = 5.0 ! BioBB simulation_type npt")
            mdin_list.append("  pres0 = 1.0 ! BioBB simulation_type npt")
            mdin_list.append("  ntp = 1 ! BioBB simulation_type npt")
            mdin_list.append("  taup = 2.0 ! BioBB simulation_type npt")
            mdin_list.append("  ntx = 5 ! BioBB simulation_type npt")
        if nvt:
            mdin_list.append("  irest = 1 ! BioBB simulation_type nvt")
            mdin_list.append("  gamma_ln = 5.0 ! BioBB simulation_type nvt")
            mdin_list.append("  ntb = 1 ! BioBB simulation_type nvt")
            mdin_list.append("  ntx = 5 ! BioBB simulation_type nvt")
        if heat:
            mdin_list.append("  tempi = 0.0 ! BioBB simulation_type heat")
            mdin_list.append("  temp0 = 300.0 ! BioBB simulation_type heat")
            mdin_list.append("  irest = 0 ! BioBB simulation_type heat")
            mdin_list.append("  ntb = 1 ! BioBB simulation_type heat")  # periodic boundaries
            mdin_list.append("  gamma_ln = 1.0 ! BioBB simulation_type heat")
            # mdin_list.append("  nmropt = 1 ! BioBB simulation_type heat")

            # mdin_lastPart.append("/")
            # mdin_lastPart.append("&wt")
            # mdin_lastPart.append(" TYPE = 'TEMP0' ! BioBB simulation_type heat")
            # mdin_lastPart.append(" ISTEP1 = 1 ! BioBB simulation_type heat")
            # mdin_lastPart.append(" ISTEP2 = 4000 ! BioBB simulation_type heat")
            # mdin_lastPart.append(" VALUE1 = 10.0 ! BioBB simulation_type heat")
            # mdin_lastPart.append(" VALUE2 = 300.0 ! BioBB simulation_type heat")
            # mdin_lastPart.append("/")
            # mdin_lastPart.append("&wt")
            # mdin_lastPart.append(" TYPE = 'END' ! BioBB simulation_type heat")
            # mdin_lastPart.append("/")

    if (not direct_mdin):

        # Adding the rest of parameters in the config file to the mdin file
        # if the parameter has already been added replace the value
        parameter_keys = [parameter.split('=')[0].strip() for parameter in mdin_list]
        for k, v in mdin.items():
            config_parameter_key = str(k).strip()
            if config_parameter_key in parameter_keys:
                mdin_list[parameter_keys.index(config_parameter_key)] = '  ' + config_parameter_key + ' = ' + str(v) + ' ! BioBB property'
            else:
                mdin_list.append('  ' + config_parameter_key + ' = '+str(v) + ' ! BioBB property')

        # Writing MD configuration file (mdin)
        with open(path, 'w') as mdin_file:
            # Start of file keyword(s)
            if mdin_firstPart:
                for line in mdin_firstPart:
                    mdin_file.write(line + '\n')

            # MD config parameters
            for line in mdin_list:
                mdin_file.write(line + '\n')

            # End of file keyword(s)
            if mdin_lastPart:
                for line in mdin_lastPart:
                    mdin_file.write(line + '\n')
            else:
                mdin_file.write("&end\n")
    else:
        # Copying generated output file to the final (user-given) file name
        shutil.copy2(input_mdin_path, path)

    return path
