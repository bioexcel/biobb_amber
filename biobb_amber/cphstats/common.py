"""Common functions for the cphstats blocks"""

from typing import List

from biobb_common.generic.biobb_object import BiobbObject


def stats_cmd(block: BiobbObject, in_key: str, out_key: str) -> List[str]:
    """Go from a cphstats_run or cestats_run block to its command without the flags of its own properties:
    the in (cpin/cein) and out (cpout/ceout) inputs named **in_key** and **out_key**, the outputs and the shared properties."""
    stage_in, stage_out = block.stage_io_dict["in"], block.stage_io_dict["out"]
    cmd = [block.binary_path,
           '-O',
           '-i', stage_in[in_key],
           '-o', stage_out['output_dat_path'],
           stage_in[out_key]
           ]

    if block.io_dict['out']['output_population_path']:
        cmd.append('--population')
        cmd.append(stage_out['output_population_path'])

    if block.io_dict['out']['output_chunk_path']:
        cmd.append('--chunk-out')
        cmd.append(stage_out['output_chunk_path'])
        if block.chunk_window:
            cmd.append('--chunk')
            cmd.append(str(block.chunk_window))

    if block.io_dict['out']['output_cumulative_path']:
        cmd.append('--cumulative-out')
        cmd.append(stage_out['output_cumulative_path'])

    if block.io_dict['out']['output_conditional_path']:
        cmd.append('--conditional-output')
        cmd.append(stage_out['output_conditional_path'])

    if block.io_dict['out']['output_chunk_conditional_path']:
        cmd.append('--chunk-conditional')
        cmd.append(stage_out['output_chunk_conditional_path'])

    if block.verbose:
        cmd.append('-v 1')

    if block.interval:
        cmd.append('-n')
        cmd.append(str(block.interval))

    if block.running_avg_window:
        cmd.append('-r')
        cmd.append(str(block.running_avg_window))

    if block.cumulative:
        cmd.append('--cumulative')

    if block.fix_remd:
        cmd.append('--fix-remd')
        cmd.append(str(block.fix_remd))

    if block.conditional:
        cmd.append('-c')
        cmd.append(str(block.conditional))

    return cmd
