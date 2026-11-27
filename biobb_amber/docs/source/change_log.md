# Biobb Amber changelog

## [Unreleased]

## What's new in version [5.4.0](https://github.com/bioexcel/biobb_amber/releases/tag/v5.4.0)?

### Changes

* [UPDATE] Update to biobb_common 5.4.0.
* [FIX] `cphstats_run` and `cestats_run`: the `timestep` property is passed to cphstats/cestats (`-t`): it was documented but never reached them. The Python example of `cestats_run` imports it from its module, `biobb_amber.cphstats.cestats_run`.
* [FIX] `pmemd_mdrun`: a `restraintmask` given in the `mdin` property is written quoted in the mdin file, as `sander_mdrun` already did. Unquoted, the Amber programs stop reading the mdin file ("Fortran runtime error: End of file"). The `simulation_type` documentation of `pmemd_mdrun` lists `heat`, which it already supported, and links to the existing sample mdin files.
* [FIX] `sander_mdrun` and `pmemd_mdrun`: the `simulation_type` value is read in any case, so the documented `NVT` gets the NVT equilibration defaults. Before, only `nvt` did: `NVT` silently wrote an mdin file without them.
* [FIX] `leap_gen_top`, `leap_solvate`, `leap_add_ions` and `leap_build_linear_structure`: the default force fields work in containers (they were sourced as `leaprc.leaprc.<name>`), and the blocks no longer fail with a `TypeError` when `AMBERHOME` is not set.
* [FIX] `leap_solvate` and `leap_add_ions`: the TIP4P-Ew and TIP4P-D water models are sourced in the leap input; the `source` command was missing and tleap failed.
* [FIX] `process_mdout` and `process_minout` no longer delete the `summary*` files of the folder they run from.
* [FIX] `sander_mdrun` and `pmemd_mdrun`: the `mpi_flags` property reaches the MPI launcher as given; it was split into single characters.
* [FEATURE] `sander_mdrun` and `pmemd_mdrun`: the provenance of a step skipped by the `restart` property records the parameters of its mdin file.
* [DOCS] `amber_to_pdb`, `cestats_run`, `cphstats_run`, `cpptraj_randomize_ions`, `sander_mdrun` and `pmemd_mdrun` document every file format they accept, in the docstrings and the JSON schemas.
* [UPDATE] Python 3.11 to 3.13.

## What's new in version [5.3.3](https://github.com/bioexcel/biobb_amber/releases/tag/v5.3.3)?

### Changes

* [FIX] Bug fix related to containers execution in LeapAddIons and LeapSolvate

## What's new in version [5.3.2](https://github.com/bioexcel/biobb_amber/releases/tag/v5.3.2)?

### Changes

* [FIX] Bug fix related to containers execution in LeapGenTop

## What's new in version [5.3.1](https://github.com/bioexcel/biobb_amber/releases/tag/v5.3.1)?

### Changes

* [UPDATE] Update to biobb_common 5.3.1

## What's new in version [5.2.1](https://github.com/bioexcel/biobb_amber/releases/tag/v5.2.1)?

### Changes

* [UPDATE] Update to biobb_common 5.2.2

## What's new in version [5.2.0](https://github.com/bioexcel/biobb_amber/releases/tag/v5.2.0)?

### Changes

* [UPDATE] Update to biobb_common 5.2.0

## What's new in version [5.1.0](https://github.com/bioexcel/biobb_amber/releases/tag/v5.1.0)?

### Changes

* [UPDATE] Update to biobb_common 5.1.0
* [UPDATE] Update to Ambertools >= 22.5 
* [UPDATE] Removed NAB tool, discontinued in newest versions of Ambertools

## What's new in version [5.0.4](https://github.com/bioexcel/biobb_amber/releases/tag/v5.0.4)?

### Changes

* [FEATURE](leap): Added support for downloaded or old force fields

## What's new in version [5.0.3](https://github.com/bioexcel/biobb_amber/releases/tag/v5.0.3)?

### Changes

* [FIX](all): Accept lists in different formats for input parameters.

## What's new in version [5.0.2](https://github.com/bioexcel/biobb_amber/releases/tag/v5.0.2)?

### Changes

* [FEATURE](leap): Adding new input
* [FIX](leap): Ions in 4p wat bug fixed; loadAmberPrep added in leap bbs

## What's new in version [5.0.0](https://github.com/bioexcel/biobb_amber/releases/tag/v5.0.0)?

### Changes

* [FEATURE](__init__): Importing submodules when a module is loaded
* [UPDATE] Adding sandbox_path property to the json schemas
* [FEATURE] New sandbox_path property
* [FEATURE] Adding direct_mdin option

## What's new in version [4.2.0](https://github.com/bioexcel/biobb_amber/releases/tag/v4.2.0)?
In version 4.2.0 the dependency biobb_common has been updated to 4.2.0 version.

### New features

* Update to biobb_common 4.2.0 (general)

## What's new in version [4.1.0](https://github.com/bioexcel/biobb_amber/releases/tag/v4.1.0)?
In version 4.1.0 the dependency biobb_common has been updated to 4.1.0 version.

### New features

* Update to biobb_common 4.1.0 (general)

## What's new in version [4.0.1](https://github.com/bioexcel/biobb_amber/releases/tag/v4.0.1)?
In version 4.0.1 some minor bugs have been fixed in leap submodule.

### New features

* Minor bug fixes (leap)

## What's new in version [4.0.0](https://github.com/bioexcel/biobb_amber/releases/tag/v4.0.0)?
In version 4.0.0 the dependency biobb_common has been updated to 4.0.0 version.

### New features

* Update to biobb_common 4.0.0 (general)

## What's new in version [3.9.0](https://github.com/bioexcel/biobb_amber/releases/tag/v3.9.0)?
In version 3.9.0 the dependency biobb_common has been updated to 3.9.0 version.

### New features

* Update to biobb_common 3.9.0 (general)
* All inputs/outputs are checked for correct file format, extension and type (general)

## What's new in version [3.8.0](https://github.com/bioexcel/biobb_amber/releases/tag/v3.8.0)?
In version 3.8.0 the dependency biobb_common has been updated to 3.8.1 version.

### New features

* Update to biobb_common 3.8.1 (general)

## What's new in version [3.7.1](https://github.com/bioexcel/biobb_amber/releases/tag/v3.7.1)?
In version 3.7.1 entry points have been added to setup.py.

## What's new in version [3.7.0](https://github.com/bioexcel/biobb_amber/releases/tag/v3.7.0)?
In version 3.7.0 the dependency biobb_common has been updated to 3.7.0 version.

### New features

* Update to biobb_common 3.7.0 (general)

## What's new in version [3.6.2](https://github.com/bioexcel/biobb_amber/releases/tag/v3.6.2)?
In version 3.6.2 some bugs have been fixed.

### New features

* Sander/Pmemd mdin parser upgraded

## What's new in version [3.6.1](https://github.com/bioexcel/biobb_amber/releases/tag/v3.6.1)?
In version 3.6.1 some bugs have been fixed.

### Other changes

* Bug fixes

## What's new in version [3.6.0](https://github.com/bioexcel/biobb_amber/releases/tag/v3.6.0)?
In version 3.6.0 the dependency biobb_common has been updated to 3.6.0 version.

### New features

* Update to biobb_common 3.6.0 (general)

## What's new in version [3.5.0](https://github.com/bioexcel/biobb_amber/releases/tag/v3.5.0)?
New package wrapping AMBER MD tool. In version 3.5.0 the dependency biobb_common has been updated to 3.5.1 version. Also, there has been implemented the new version of docstrings, therefore the JSON Schemas have been modified.

### New features

* New Package biobb_amber
* Update to biobb_common 3.5.1 (general)
* New extended and improved JSON schemas (Galaxy and CWL-compliant) (general)

### Other changes

* New docstrings
