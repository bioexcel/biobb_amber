"""Common functions for the leap blocks"""

import os
from typing import List, Optional


def leaprc_files(forcefields: List[str], container_path: Optional[str] = None) -> List[str]:
    """Go from the forcefield property (force field names or leaprc paths) to the files that tleap
    sources: ``leaprc.<name>`` in a container, else the paths found in ``$AMBERHOME/dat/leap/cmd``."""
    if container_path:
        return [f"leaprc.{forcefield}" for forcefield in forcefields]
    cmd_dir = os.path.join(os.environ.get("AMBERHOME", ""), "dat", "leap", "cmd")
    leaprc_paths = []
    for forcefield in forcefields:
        # A path, else a file of cmd or cmd/oldff, with or without the leaprc. prefix
        candidates = [forcefield] + [os.path.join(cmd_dir, folder, name)
                                     for name in (f"leaprc.{forcefield}", forcefield) for folder in ("", "oldff")]
        leaprc_path = next((path for path in candidates if os.path.exists(path)), None)
        if leaprc_path is None:
            raise ValueError(f"Force field {forcefield} not found. Check the $AMBERHOME/dat/leap/cmd/ directory for available force fields or provide the path to an existing leaprc file.")
        leaprc_paths.append(leaprc_path)
    return leaprc_paths
