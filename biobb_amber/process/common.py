"""Common functions for package biobb_amber.process"""

from pathlib import Path, PurePath
from typing import Optional, Union

from biobb_common.tools import file_utils as fu


# CHECK INPUT PARAMETERS
def check_input_path(path, argument, optional, out_log, classname):
    """Checks input file"""
    if optional and not path:
        return None
    if not Path(path).exists():
        fu.log(classname + ": Unexisting %s file, exiting" % argument, out_log)
        raise SystemExit(classname + ": Unexisting %s file" % argument)
    file_extension = PurePath(path).suffix
    if not is_valid_file(file_extension[1:], argument):
        fu.log(
            classname + ": Format %s in %s file is not compatible"
            % (file_extension[1:], argument),
            out_log,
        )
        raise SystemExit(
            classname + ": Format %s in %s file is not compatible"
            % (file_extension[1:], argument)
        )
    return path


# CHECK OUTPUT PARAMETERS
def check_output_path(path, argument, optional, out_log, classname):
    """Checks output file"""
    if optional and not path:
        return None
    if PurePath(path).parent and not Path(PurePath(path).parent).exists():
        fu.log(classname + ": Unexisting  %s folder, exiting" % argument, out_log)
        raise SystemExit(classname + ": Unexisting  %s folder" % argument)
    file_extension = PurePath(path).suffix
    if not is_valid_file(file_extension[1:], argument):
        fu.log(
            classname + ": Format %s in  %s file is not compatible"
            % (file_extension[1:], argument),
            out_log,
        )
        raise SystemExit(
            classname + ": Format %s in  %s file is not compatible"
            % (file_extension[1:], argument)
        )
    return path


def is_valid_file(ext, argument):
    """Checks if file format is compatible"""
    formats = {
        "input_log_path": ["log", "out", "txt", "o"],
        "output_dat_path": ["dat", "txt", "csv"],
    }
    return ext in formats[argument]


def _from_string_to_list(input_data: Optional[Union[str, list[str]]]) -> list[str]:
    """
    Converts a string to a list, splitting by commas or spaces. If the input is already a list, returns it as is.
    Returns an empty list if input_data is None.

    Parameters:
        input_data (str, list, or None): The string, list, or None value to convert.

    Returns:
        list: A list of string elements or an empty list if input_data is None.
    """
    if input_data is None:
        return []

    if isinstance(input_data, list):
        # If input is already a list, return it
        return input_data

    # If input is a string, determine the delimiter based on presence of commas
    delimiter = "," if "," in input_data else " "
    items = input_data.split(delimiter)

    # Remove whitespace from each item and ignore empty strings
    processed_items = [item.strip() for item in items if item.strip()]

    return processed_items
