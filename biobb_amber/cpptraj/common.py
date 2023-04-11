""" Common functions for package biobb_amber.cpptraj """
from pathlib import Path, PurePath
from biobb_common.tools import file_utils as fu


# CHECK INPUT PARAMETERS
def check_input_path(path, argument, optional, out_log, classname):
    """ Checks input file """
    if optional and not path:
        return None
    if not Path(path).exists():
        fu.log(classname + ': Unexisting %s file, exiting' % argument, out_log)
        raise SystemExit(classname + ': Unexisting %s file' % argument)
    file_extension = PurePath(path).suffix
    if not is_valid_file(file_extension[1:], argument):
        fu.log(classname + ': Format %s in %s file is not compatible' % (file_extension[1:], argument), out_log)
        raise SystemExit(classname + ': Format %s in %s file is not compatible' % (file_extension[1:], argument))
    return path


# CHECK OUTPUT PARAMETERS
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
        'input_crd_path': ['crd', 'mdcrd', 'inpcrd', 'rst', 'rst7'],
        'input_top_path': ['top', 'prmtop', 'parmtop'],
        'output_pdb_path': ['pdb'],
        'output_crd_path': ['crd', 'mdcrd', 'inpcrd', 'rst', 'rst7']
    }
    return ext in formats[argument]
