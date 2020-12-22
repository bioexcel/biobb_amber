#!/usr/bin/env python3

"""Module containing the Template class and the command line interface."""
import argparse
import shutil
from pathlib import Path, PurePath
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper

# 1. Rename class as required
class Template():
    """Description for the template (http://templatedocumentation.org) module.

    Args:
        input_file_path1 (str): Description for the first input file path. File type: input. `Sample file <https://urlto.sample>`_. Accepted formats: top.
        input_file_path2 (str) (Optional): Description for the second input file path (optional). File type: input. `Sample file <https://urlto.sample>`_. Accepted formats: dcd.
        output_file_path (str): Description for the output file path. File type: output. `Sample file <https://urlto.sample>`_. Accepted formats: zip.
        properties (dic):
            * **boolean_property** (*bool*) - (True) Example of boolean property.
            * **executable_binary_property** (*str*) - ("zip") Example of executable binary property.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
    """

    # 2. Adapt input and output file paths as required. Include all files, even optional ones
    def __init__(self, input_file_path1, input_file_path2, output_file_path, properties, **kwargs):
        properties = properties or {}

        # 2.1 Modify to match constructor parameters
        # Input/Output files
        self.io_dict = { 
            'in': { 'input_file_path1': input_file_path1, 'input_file_path2': input_file_path2 }, 
            'out': { 'output_file_path': output_file_path } 
        }

        # 3. Include all relevant properties here as 
        # self.property_name = properties.get('property_name', property_default_value)

        # Properties specific for BB
        self.properties = properties
        self.boolean_property = properties.get('boolean_property', True)
        self.executable_binary_property = properties.get('executable_binary_property', 'zip')

        # Properties common in all BB
        self.can_write_console_log = properties.get('can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')
        self.remove_tmp = properties.get('remove_tmp', True)
        self.restart = properties.get('restart', False)

    @launchlogger
    def launch(self):
        """Launches the execution of the template module."""
        
        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        # Check the properties
        fu.check_properties(self, self.properties)

        # Restart
        if self.restart:
            # 4. Include here all output file paths
            output_file_list = [self.io_dict['out']['output_file_path']]
            if fu.check_complete_files(output_file_list):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step, out_log, self.global_log)
                return 0

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir()
        fu.log('Creating %s temporary folder' % self.tmp_folder, out_log)

        # 5. Include here all mandatory input files
        # Copy input_file_path1 to temporary folder
        shutil.copy(self.io_dict['in']['input_file_path1'], self.tmp_folder)

        # 6. Prepare the command line parameters as instructions list
        instructions = ['-j']
        if self.boolean_property:
            instructions.append('-v')
            fu.log('Appending optional boolean property', out_log, self.global_log)

        # 7. Build the actual command line as a list of items (elements order will be maintained)
        cmd = [self.executable_binary_property,
               ' '.join(instructions), 
               self.io_dict['out']['output_file_path'],
               str(PurePath(self.tmp_folder).joinpath(PurePath(self.io_dict['in']['input_file_path1']).name))]
        fu.log('Creating command line with instructions and required arguments', out_log, self.global_log)

        # 8. Repeat for optional input files if provided
        if self.io_dict['in']['input_file_path2']:
            # Copy input_file_path2 to temporary folder
            shutil.copy(self.io_dict['in']['input_file_path2'], self.tmp_folder)
            # Append optional input_file_path2 to cmd
            cmd.append(str(PurePath(self.tmp_folder).joinpath(PurePath(self.io_dict['in']['input_file_path2']).name)))
            fu.log('Appending optional argument to command line', out_log, self.global_log)

        # 9. Uncomment to check the command line 
        # print(' '.join(cmd))

        # Launch execution
        returncode = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()

        # Remove temporary file(s)
        if self.remove_tmp: 
            fu.rm(self.tmp_folder)
            fu.log('Removed: %s' % str(self.tmp_folder), out_log)

        return returncode

def main():
    parser = argparse.ArgumentParser(description='Description for the template module.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # 10. Include specific args of each building block following the examples. They should match step 2
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_file_path1', required=True, help='Description for the first input file path. Accepted formats: top.')
    parser.add_argument('--input_file_path2', required=False, help='Description for the second input file path (optional). Accepted formats: dcd.')
    required_args.add_argument('--output_file_path', required=True, help='Description for the output file path. Accepted formats: zip.')

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # 11. Adapt to match Class constructor (step 2)
    # Specific call of each building block
    Template(input_file_path1=args.input_file_path1, input_file_path2=args.input_file_path2, 
             output_file_path=args.output_file_path, 
             properties=properties).launch()

if __name__ == '__main__':
    main()

# 12. Complete documentation strings