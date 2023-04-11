#!/usr/bin/env python3

""" Common functions for package biobb_amber.sander """
from pathlib import Path, PurePath
from biobb_common.tools import file_utils as fu


# CHECK INPUT PARAMETERS
def check_input_path(path, argument, optional, out_log, classname):
    """ Checks input file """
    if optional and not path:
        return None
    if not Path(path).exists():
        fu.log("Path: " + path)
        fu.log("Path " + path + " --- " + classname + ': Unexisting %s file, exiting' % argument, out_log)
        raise SystemExit(classname + ': Unexisting %s file' % argument)
    file_extension = PurePath(path).suffix
    if not is_valid_file(file_extension[1:], argument):
        fu.log(classname + ': Format %s in %s file is not compatible' % (file_extension[1:], argument), out_log)
        raise SystemExit(classname + ': Format %s in %s file is not compatible' % (file_extension[1:], argument))
    return path


def check_output_path(path, argument, optional, out_log, classname):
    """ Checks output file """
    if optional and not path:
        return None
    if PurePath(path).parent and not Path(PurePath(path).parent).exists():
        fu.log(classname + ': Unexisting  %s folder, exiting' % argument, out_log)
        raise SystemExit(classname + ': Unexisting  %s folder' % argument)
    file_extension = PurePath(path).suffix
    if not is_valid_file(file_extension[1:], argument):
        fu.log(classname + ': Format %s in  %s file is not compatible' % (file_extension[1:], argument), out_log)
        raise SystemExit(classname + ': Format %s in  %s file is not compatible' % (file_extension[1:], argument))
    return path


def is_valid_file(ext, argument):
    """ Checks if file format is compatible """
    formats = {
        'input_top_path': ['top', 'prmtop', 'parmtop'],
        'input_crd_path': ['crd', 'inpcrd', 'mdcrd', 'rst', 'rst7', 'netcdf', 'nc', 'ncrst'],
        'input_mdin_path': ['mdin', 'txt', 'in'],
        'input_cpin_path': ['cpin', 'txt', 'in'],
        'input_ref_path': ['crd', 'inpcrd', 'mdcrd', 'rst', 'rst7', 'netcdf', 'nc', 'ncrst'],
        'output_log_path': ['log', 'out', 'txt', 'o'],
        'output_traj_path': ['trj', 'crd', 'mdcrd', 'x', 'netcdf', 'nc'],
        'output_rst_path': ['rst', 'rst7', 'netcdf', 'nc', 'ncrst'],
        'output_cpout_path': ['cpout'],
        'output_cprst_path': ['cprst', 'rst', 'rst7'],
        'output_mdinfo_path': ['mdinfo']
    }
    return ext in formats[argument]
