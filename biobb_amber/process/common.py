"""Common functions for the process blocks"""

import shutil
from pathlib import Path
from typing import Dict, List


def summaries_to_dat(summary_dir: str, terms: List[str], output_dat_path: str) -> None:
    """Go from the ``summary.<term>`` files that process_mdout.perl and process_minout.perl write in
    **summary_dir** to one dat file: the summary file itself for one term, else a table by time."""
    if len(terms) == 1:
        shutil.copy(Path(summary_dir).joinpath("summary." + terms[0]), output_dat_path)
        return
    ene_dict: Dict[float, Dict[str, str]] = {}
    for term in terms:
        with open(Path(summary_dir).joinpath("summary." + term)) as fp:
            for line in fp:
                x = line.split()
                if x:
                    ene_dict.setdefault(float(x[0]), {})[term] = x[1] if len(x) > 1 else "-"

    with open(output_dat_path, "w") as fp_out:
        fp_out.write("# TIME " + "".join(term + " " for term in terms) + "\n")
        for key in sorted(ene_dict):
            fp_out.write(str(key) + " " + "".join(ene_dict[key][term] + " " for term in terms) + "\n")
