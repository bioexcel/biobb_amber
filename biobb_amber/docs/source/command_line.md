# BioBB AMBER Command Line Help
Generic usage:
```python
biobb_command [-h] --config CONFIG --input_file(s) <input_file(s)> --output_file <output_file>
```
-----------------


## Leap_solvate
Wrapper of the AmberTools (AMBER MD Package) leap tool module.
### Get help
Command:
```python
leap_solvate -h
```
    /bin/sh: leap_solvate: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input 3D structure PDB file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/structure.leap.pdb). Accepted formats: PDB
* **input_lib_path** (*string*): Input ligand library parameters file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/ligand.lib). Accepted formats: LIB, ZIP
* **input_frcmod_path** (*string*): Input ligand frcmod parameters file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/ligand.frcmod). Accepted formats: FRCMOD, ZIP
* **input_params_path** (*string*): Additional leap parameter files to load with loadAmberParams Leap command. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/frcmod.ionsdang_spce). Accepted formats: IN, LEAPIN, TXT, ZIP
* **input_source_path** (*string*): Additional leap command files to load with source Leap command. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/leaprc.water.spce). Accepted formats: IN, LEAPIN, TXT, ZIP
* **output_pdb_path** (*string*): Output 3D structure PDB file matching the topology file. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.solv.pdb). Accepted formats: PDB
* **output_top_path** (*string*): Output topology file (AMBER ParmTop). File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.solv.top). Accepted formats: TOP, PARMTOP, PRMTOP
* **output_crd_path** (*string*): Output coordinates file (AMBER crd). File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.solv.crd). Accepted formats: CRD, MDCRD, INPCRD
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **forcefield** (*array*): ([protein.ff14SB,DNA.bsc1,gaff]) Forcefield to be used for the structure generation. .
* **water_type** (*string*): (TIP3PBOX) Water molecule parameters to be used for the topology. .
* **box_type** (*string*): (truncated_octahedron) Type for the MD system box. .
* **ions_type** (*string*): (ionsjc_tip3p) Ions type. .
* **neutralise** (*boolean*): (False) Energetically neutralise the system adding the necessary counterions..
* **iso** (*boolean*): (False) Make the box isometric..
* **positive_ions_number** (*integer*): (0) Number of additional positive ions to include in the system box..
* **negative_ions_number** (*integer*): (0) Number of additional negative ions to include in the system box..
* **positive_ions_type** (*string*): (Na+) Type of additional positive ions to include in the system box. .
* **negative_ions_type** (*string*): (Cl-) Type of additional negative ions to include in the system box. .
* **distance_to_molecule** (*number*): (8.0) Size for the MD system box, defined such as the minimum distance between any atom originally present in solute and the edge of the periodic box is given by this distance parameter..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_leap_solvate.yml)
```python
properties:
  box_type: truncated_octahedron
  distance_to_molecule: '9.0'
  forcefield:
  - protein.ff14SB
  remove_tmp: true
  water_type: TIP3PBOX

```
#### Command line
```python
leap_solvate --config config_leap_solvate.yml --input_pdb_path structure.leap.pdb --input_lib_path ligand.lib --input_frcmod_path ligand.frcmod --input_params_path frcmod.ionsdang_spce --input_source_path leaprc.water.spce --output_pdb_path structure.solv.pdb --output_top_path structure.solv.top --output_crd_path structure.solv.crd
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_leap_solvate.json)
```python
{
  "properties": {
    "forcefield": [
      "protein.ff14SB"
    ],
    "water_type": "TIP3PBOX",
    "distance_to_molecule": "9.0",
    "box_type": "truncated_octahedron",
    "remove_tmp": true
  }
}
```
#### Command line
```python
leap_solvate --config config_leap_solvate.json --input_pdb_path structure.leap.pdb --input_lib_path ligand.lib --input_frcmod_path ligand.frcmod --input_params_path frcmod.ionsdang_spce --input_source_path leaprc.water.spce --output_pdb_path structure.solv.pdb --output_top_path structure.solv.top --output_crd_path structure.solv.crd
```

## Sander_mdrun
Wrapper of the AmberTools (AMBER MD Package) sander tool module.
### Get help
Command:
```python
sander_mdrun -h
```
    /bin/sh: sander_mdrun: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_top_path** (*string*): Input topology file (AMBER ParmTop). File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/sander/cln025.prmtop). Accepted formats: TOP, PARMTOP, PRMTOP
* **input_crd_path** (*string*): Input coordinates file (AMBER crd). File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/sander/cln025.inpcrd). Accepted formats: CRD, MDCRD, INPCRD
* **input_mdin_path** (*string*): Input configuration file (MD run options) (AMBER mdin). File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/sander/npt.mdin). Accepted formats: MDIN, IN, TXT
* **input_cpin_path** (*string*): Input constant pH file (AMBER cpin). File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/sander/cln025.cpin). Accepted formats: CPIN
* **input_ref_path** (*string*): Input reference coordinates for position restraints. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/sander/sander.rst). Accepted formats: RST, RST7
* **output_log_path** (*string*): Output log file. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/sander/sander.log). Accepted formats: LOG, OUT, TXT, O
* **output_traj_path** (*string*): Output trajectory file. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/sander/sander.x). Accepted formats: TRJ, CRD, MDCRD, X, NETCDF, NC
* **output_rst_path** (*string*): Output restart file. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/sander/sander.rst). Accepted formats: RST, RST7
* **output_cpout_path** (*string*): Output constant pH file (AMBER cpout). File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/sander/sander.cpout). Accepted formats: CPOUT
* **output_cprst_path** (*string*): Output constant pH restart file (AMBER rstout). File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/sander/sander.cprst). Accepted formats: CPRST, RST, RST7
* **output_mdinfo_path** (*string*): Output MD info. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/sander/sander.mdinfo). Accepted formats: MDINFO
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **mdin** (*object*): ({}) Sander MD run options specification. (Used if *input_mdin_path* is None).
* **simulation_type** (*string*): (minimization) Default options for the mdin file. Each creates a different mdin file. .
* **sander_path** (*string*): (sander) sander binary path to be used..
* **mpi_bin** (*string*): (None) Path to the MPI runner. Usually "mpirun" or "srun"..
* **mpi_np** (*integer*): (0) Number of MPI processes. Usually an integer bigger than 1..
* **mpi_hostlist** (*string*): (None) Path to the MPI hostlist file..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_sander_mdrun.yml)
```python
properties:
  mdin:
    ioutfm: 0
    maxcyc: 500
    ntwx: 100
  remove_tmp: true
  simulation_type: minimization

```
#### Command line
```python
sander_mdrun --config config_sander_mdrun.yml --input_top_path cln025.prmtop --input_crd_path cln025.inpcrd --input_mdin_path npt.mdin --input_cpin_path cln025.cpin --input_ref_path sander.rst --output_log_path sander.log --output_traj_path sander.x --output_rst_path sander.rst --output_cpout_path sander.cpout --output_cprst_path sander.cprst --output_mdinfo_path sander.mdinfo
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_sander_mdrun.json)
```python
{
  "properties": {
    "simulation_type": "minimization",
    "mdin": {
      "maxcyc": 500,
      "ntwx": 100,
      "ioutfm": 0
    },
    "remove_tmp": true
  }
}
```
#### Command line
```python
sander_mdrun --config config_sander_mdrun.json --input_top_path cln025.prmtop --input_crd_path cln025.inpcrd --input_mdin_path npt.mdin --input_cpin_path cln025.cpin --input_ref_path sander.rst --output_log_path sander.log --output_traj_path sander.x --output_rst_path sander.rst --output_cpout_path sander.cpout --output_cprst_path sander.cprst --output_mdinfo_path sander.mdinfo
```

## Pmemd_mdrun
Wrapper of the AmberTools (AMBER MD Package) pmemd tool module.
### Get help
Command:
```python
pmemd_mdrun -h
```
    /bin/sh: pmemd_mdrun: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_top_path** (*string*): Input topology file (AMBER ParmTop). File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pmemd/cln025.prmtop). Accepted formats: TOP, PARMTOP, PRMTOP
* **input_crd_path** (*string*): Input coordinates file (AMBER crd). File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pmemd/cln025.inpcrd). Accepted formats: CRD, MDCRD, INPCRD, RST, RST7
* **input_mdin_path** (*string*): Input configuration file (MD run options) (AMBER mdin). File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pmemd/npt.mdin). Accepted formats: MDIN, IN, TXT
* **input_cpin_path** (*string*): Input constant pH file (AMBER cpin). File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pmemd/cln025.cpin). Accepted formats: CPIN
* **input_ref_path** (*string*): Input reference coordinates for position restraints. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pmemd/sander.rst). Accepted formats: CRD, MDCRD, INPCRD, RST, RST7
* **output_log_path** (*string*): Output log file. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/pmemd/sander.log). Accepted formats: LOG, OUT, TXT, O
* **output_traj_path** (*string*): Output trajectory file. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/pmemd/sander.x). Accepted formats: TRJ, CRD, MDCRD, X, NETCDF, NC
* **output_rst_path** (*string*): Output restart file. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/pmemd/sander.rst). Accepted formats: RST, RST7
* **output_cpout_path** (*string*): Output constant pH file (AMBER cpout). File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/pmemd/sander.cpout). Accepted formats: CPOUT
* **output_cprst_path** (*string*): Output constant pH restart file (AMBER rstout). File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/pmemd/sander.cprst). Accepted formats: CPRST, RST, RST7
* **output_mdinfo_path** (*string*): Output MD info. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/pmemd/sander.mdinfo). Accepted formats: MDINFO
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **mdin** (*object*): ({}) pmemd MD run options specification. (Used if *input_mdin_path* is None).
* **pmemd_path** (*string*): (pmemd) pmemd binary path to be used..
* **simulation_type** (*string*): (minimization) Default options for the mdin file. Each creates a different mdin file. .
* **mpi_bin** (*string*): (None) Path to the MPI runner. Usually "mpirun" or "srun"..
* **mpi_np** (*integer*): (0) Number of MPI processes. Usually an integer bigger than 1..
* **mpi_hostlist** (*string*): (None) Path to the MPI hostlist file..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_pmemd_mdrun.yml)
```python
properties:
  mdin:
    ioutfm: 0
    maxcyc: 500
    ntwx: 100
  remove_tmp: true
  simulation_type: minimization

```
#### Command line
```python
pmemd_mdrun --config config_pmemd_mdrun.yml --input_top_path cln025.prmtop --input_crd_path cln025.inpcrd --input_mdin_path npt.mdin --input_cpin_path cln025.cpin --input_ref_path sander.rst --output_log_path sander.log --output_traj_path sander.x --output_rst_path sander.rst --output_cpout_path sander.cpout --output_cprst_path sander.cprst --output_mdinfo_path sander.mdinfo
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_pmemd_mdrun.json)
```python
{
  "properties": {
    "simulation_type": "minimization",
    "mdin": {
      "maxcyc": 500,
      "ntwx": 100,
      "ioutfm": 0
    },
    "remove_tmp": true
  }
}
```
#### Command line
```python
pmemd_mdrun --config config_pmemd_mdrun.json --input_top_path cln025.prmtop --input_crd_path cln025.inpcrd --input_mdin_path npt.mdin --input_cpin_path cln025.cpin --input_ref_path sander.rst --output_log_path sander.log --output_traj_path sander.x --output_rst_path sander.rst --output_cpout_path sander.cpout --output_cprst_path sander.cprst --output_mdinfo_path sander.mdinfo
```

## Process_mdout
Wrapper of the AmberTools (AMBER MD Package) process_mdout tool module.
### Get help
Command:
```python
process_mdout -h
```
    /bin/sh: process_mdout: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_log_path** (*string*): AMBER (sander) MD output (log) file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/process/sander.heat.log). Accepted formats: LOG, OUT, TXT, O
* **output_dat_path** (*string*): Dat output file containing data from the specified terms along the minimization process. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/process/sander.md.temp.dat). Accepted formats: DAT, TXT, CSV
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **terms** (*array*): ([ETOT]) Statistics descriptors. .
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_process_mdout.yml)
```python
properties:
  remove_tmp: true
  terms:
  - TEMP

```
#### Command line
```python
process_mdout --config config_process_mdout.yml --input_log_path sander.heat.log --output_dat_path sander.md.temp.dat
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_process_mdout.json)
```python
{
  "properties": {
    "terms": [
      "TEMP"
    ],
    "remove_tmp": true
  }
}
```
#### Command line
```python
process_mdout --config config_process_mdout.json --input_log_path sander.heat.log --output_dat_path sander.md.temp.dat
```

## Leap_add_ions
Wrapper of the AmberTools (AMBER MD Package) leap tool module.
### Get help
Command:
```python
leap_add_ions -h
```
    /bin/sh: leap_add_ions: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input 3D structure PDB file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/structure.solv.pdb). Accepted formats: PDB
* **input_lib_path** (*string*): Input ligand library parameters file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/ligand.lib). Accepted formats: LIB, ZIP
* **input_frcmod_path** (*string*): Input ligand frcmod parameters file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/ligand.frcmod). Accepted formats: FRCMOD, ZIP
* **input_params_path** (*string*): Additional leap parameter files to load with loadAmberParams Leap command. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/frcmod.ionsdang_spce). Accepted formats: IN, LEAPIN, TXT, ZIP
* **input_source_path** (*string*): Additional leap command files to load with source Leap command. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/leaprc.water.spce). Accepted formats: IN, LEAPIN, TXT, ZIP
* **output_pdb_path** (*string*): Output 3D structure PDB file matching the topology file. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.ions.pdb). Accepted formats: PDB
* **output_top_path** (*string*): Output topology file (AMBER ParmTop). File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.ions.top). Accepted formats: TOP, PARMTOP, PRMTOP
* **output_crd_path** (*string*): Output coordinates file (AMBER crd). File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.ions.crd). Accepted formats: CRD, MDCRD, INPCRD
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **forcefield** (*array*): ([protein.ff14SB,DNA.bsc1,gaff]) Forcefield to be used for the structure generation. .
* **water_type** (*string*): (TIP3PBOX) Water molecule parameters to be used for the topology. .
* **box_type** (*string*): (truncated_octahedron) Type for the MD system box. .
* **ions_type** (*string*): (ionsjc_tip3p) Ions type. .
* **neutralise** (*boolean*): (True) Energetically neutralise the system adding the necessary counterions..
* **ionic_concentration** (*number*): (0.05) Additional ionic concentration to include in the system box. Units in Mol/L..
* **positive_ions_number** (*integer*): (0) Number of additional positive ions to include in the system box..
* **negative_ions_number** (*integer*): (0) Number of additional negative ions to include in the system box..
* **positive_ions_type** (*string*): (Na+) Type of additional positive ions to include in the system box. .
* **negative_ions_type** (*string*): (Cl-) Type of additional negative ions to include in the system box. .
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_leap_add_ions.yml)
```python
properties:
  box_type: truncated_octahedron
  forcefield:
  - protein.ff14SB
  - DNA.bsc1
  ionic_concentration: 150
  negative_ions_type: Cl-
  neutralise: true
  positive_ions_type: K+
  remove_tmp: true
  water_type: TIP3PBOX

```
#### Command line
```python
leap_add_ions --config config_leap_add_ions.yml --input_pdb_path structure.solv.pdb --input_lib_path ligand.lib --input_frcmod_path ligand.frcmod --input_params_path frcmod.ionsdang_spce --input_source_path leaprc.water.spce --output_pdb_path structure.ions.pdb --output_top_path structure.ions.top --output_crd_path structure.ions.crd
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_leap_add_ions.json)
```python
{
  "properties": {
    "forcefield": [
      "protein.ff14SB",
      "DNA.bsc1"
    ],
    "water_type": "TIP3PBOX",
    "box_type": "truncated_octahedron",
    "neutralise": true,
    "positive_ions_type": "K+",
    "negative_ions_type": "Cl-",
    "ionic_concentration": 150,
    "remove_tmp": true
  }
}
```
#### Command line
```python
leap_add_ions --config config_leap_add_ions.json --input_pdb_path structure.solv.pdb --input_lib_path ligand.lib --input_frcmod_path ligand.frcmod --input_params_path frcmod.ionsdang_spce --input_source_path leaprc.water.spce --output_pdb_path structure.ions.pdb --output_top_path structure.ions.top --output_crd_path structure.ions.crd
```

## Process_minout
Wrapper of the AmberTools (AMBER MD Package) process_minout tool module.
### Get help
Command:
```python
process_minout -h
```
    /bin/sh: process_minout: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_log_path** (*string*): AMBER (sander) Minimization output (log) file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/process/sander.min.log). Accepted formats: LOG, OUT, TXT, O
* **output_dat_path** (*string*): Dat output file containing data from the specified terms along the minimization process. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/process/sander.min.energy.dat). Accepted formats: DAT, TXT, CSV
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **terms** (*array*): ([ENERGY]) Statistics descriptors. .
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_process_minout.yml)
```python
properties:
  remove_tmp: true

```
#### Command line
```python
process_minout --config config_process_minout.yml --input_log_path sander.min.log --output_dat_path sander.min.energy.dat
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_process_minout.json)
```python
{
  "properties": {
    "remove_tmp": true
  }
}
```
#### Command line
```python
process_minout --config config_process_minout.json --input_log_path sander.min.log --output_dat_path sander.min.energy.dat
```

## Leap_build_linear_structure
Wrapper of the AmberTools (AMBER MD Package) leap tool module.
### Get help
Command:
```python
leap_build_linear_structure -h
```
    /bin/sh: leap_build_linear_structure: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **output_pdb_path** (*string*): Linear (unfolded) 3D structure PDB file. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **sequence** (*string*): (ALA GLY SER PRO ARG ALA PRO GLY) Aminoacid sequence to convert to a linear 3D structure. Aminoacids should be written in 3-letter code, with a blank space between them..
* **forcefield** (*array*): ([protein.ff14SB,DNA.bsc1,gaff]) Forcefield to be used for the structure generation. .
* **build_library** (*boolean*): (False) Generate AMBER lib file for the structure..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_leap_build_linear_structure.yml)
```python
properties:
  build_library: false
  forcefield:
  - protein.ff14SB
  remove_tmp: true
  sequence: ALA PRO SER ARG LYS ASP GLU GLY GLY ALA

```
#### Command line
```python
leap_build_linear_structure --config config_leap_build_linear_structure.yml --output_pdb_path structure.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_leap_build_linear_structure.json)
```python
{
  "properties": {
    "sequence": "ALA PRO SER ARG LYS ASP GLU GLY GLY ALA",
    "build_library": false,
    "forcefield": [
      "protein.ff14SB"
    ],
    "remove_tmp": true
  }
}
```
#### Command line
```python
leap_build_linear_structure --config config_leap_build_linear_structure.json --output_pdb_path structure.pdb
```

## Nab_build_dna_structure
Wrapper of the AmberTools (AMBER MD Package) nab tool module.
### Get help
Command:
```python
nab_build_dna_structure -h
```
    /bin/sh: nab_build_dna_structure: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **output_pdb_path** (*string*): DNA 3D structure PDB file. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/nab/ref_nab_build_dna_structure.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **sequence** (*string*): (GCGCGGCTGATAAACGAAAGC) Nucleotide sequence to convert to a 3D structure. Nucleotides should be written in 1-letter code, with no spaces between them..
* **helix_type** (*string*): (lbdna) DNA/RNA helix type. .
* **compiler** (*string*): (gcc) Alternative C compiler for nab..
* **linker** (*string*): (gfortran) Alternative Fortran linker for nab..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_nab_build_dna_structure.yml)
```python
properties:
  remove_tmp: true
  sequence: GCGCGGCTGATAAACGAAAGC

```
#### Command line
```python
nab_build_dna_structure --config config_nab_build_dna_structure.yml --output_pdb_path ref_nab_build_dna_structure.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_nab_build_dna_structure.json)
```python
{
  "properties": {
    "sequence": "GCGCGGCTGATAAACGAAAGC",
    "remove_tmp": true
  }
}
```
#### Command line
```python
nab_build_dna_structure --config config_nab_build_dna_structure.json --output_pdb_path ref_nab_build_dna_structure.pdb
```

## Parmed_hmassrepartition
Wrapper of the AmberTools (AMBER MD Package) parmed tool module.
### Get help
Command:
```python
parmed_hmassrepartition -h
```
    /bin/sh: parmed_hmassrepartition: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_top_path** (*string*): Input AMBER topology file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/parmed/input.hmass.prmtop). Accepted formats: TOP, PARMTOP, PRMTOP
* **output_top_path** (*string*): Output topology file (AMBER ParmTop). File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/parmed/output.hmass.prmtop). Accepted formats: TOP, PARMTOP, PRMTOP
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_parmed_hmassrepartition.yml)
```python
properties:
  remove_tmp: true

```
#### Command line
```python
parmed_hmassrepartition --config config_parmed_hmassrepartition.yml --input_top_path input.hmass.prmtop --output_top_path output.hmass.prmtop
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_parmed_hmassrepartition.json)
```python
{
  "properties": {
    "remove_tmp": true
  }
}
```
#### Command line
```python
parmed_hmassrepartition --config config_parmed_hmassrepartition.json --input_top_path input.hmass.prmtop --output_top_path output.hmass.prmtop
```

## Cpptraj_randomize_ions
Wrapper of the AmberTools (AMBER MD Package) cpptraj tool module.
### Get help
Command:
```python
cpptraj_randomize_ions -h
```
    /bin/sh: cpptraj_randomize_ions: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_top_path** (*string*): Input topology file (AMBER ParmTop). File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/cpptraj/structure.ions.parmtop). Accepted formats: TOP, PARMTOP, PRMTOP
* **input_crd_path** (*string*): Input coordinates file (AMBER crd). File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/cpptraj/structure.ions.crd). Accepted formats: CRD, MDCRD, INPCRD
* **output_pdb_path** (*string*): Structure PDB file with randomized ions. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/cpptraj/structure.randIons.pdb). Accepted formats: PDB
* **output_crd_path** (*string*): Structure CRD file with coordinates including randomized ions. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/cpptraj/structure.randIons.crd). Accepted formats: CRD, MDCRD, INPCRD
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **ion_mask** (*string*): (:K+,Cl-,Na+) Ions to be randomized. Cpptraj mask syntax can be found at the official Cpptraj manual..
* **solute_mask** (*string*): (:DA,DC,DG,DT,D?3,D?5) Solute (or set of atoms) around which the ions can get no closer than the distance specified. Cpptraj mask syntax can be found at the official Cpptraj manual..
* **distance** (*number*): (5.0) Minimum distance cutoff for the ions around the defined solute..
* **overlap** (*number*): (3.5) Minimum distance between ions..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_cpptraj_randomize_ions.yml)
```python
properties:
  remove_tmp: true

```
#### Command line
```python
cpptraj_randomize_ions --config config_cpptraj_randomize_ions.yml --input_top_path structure.ions.parmtop --input_crd_path structure.ions.crd --output_pdb_path structure.randIons.pdb --output_crd_path structure.randIons.crd
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_cpptraj_randomize_ions.json)
```python
{
  "properties": {
    "remove_tmp": true
  }
}
```
#### Command line
```python
cpptraj_randomize_ions --config config_cpptraj_randomize_ions.json --input_top_path structure.ions.parmtop --input_crd_path structure.ions.crd --output_pdb_path structure.randIons.pdb --output_crd_path structure.randIons.crd
```

## Amber_to_pdb
Wrapper of the AmberTools (AMBER MD Package) ambpdb tool module.
### Get help
Command:
```python
amber_to_pdb -h
```
    /bin/sh: amber_to_pdb: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_top_path** (*string*): AMBER topology file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/ambpdb/structure.leap.top). Accepted formats: TOP, PARMTOP, PRMTOP
* **input_crd_path** (*string*): AMBER coordinates file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/ambpdb/structure.leap.crd). Accepted formats: CRD, MDCRD, INPCRD
* **output_pdb_path** (*string*): Structure PDB file. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/ambpdb/structure.ambpdb.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_amber_to_pdb.yml)
```python
properties:
  remove_tmp: true

```
#### Command line
```python
amber_to_pdb --config config_amber_to_pdb.yml --input_top_path structure.leap.top --input_crd_path structure.leap.crd --output_pdb_path structure.ambpdb.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_amber_to_pdb.json)
```python
{
  "properties": {
    "remove_tmp": true
  }
}
```
#### Command line
```python
amber_to_pdb --config config_amber_to_pdb.json --input_top_path structure.leap.top --input_crd_path structure.leap.crd --output_pdb_path structure.ambpdb.pdb
```

## Leap_gen_top
Wrapper of the AmberTools (AMBER MD Package) leap tool module.
### Get help
Command:
```python
leap_gen_top -h
```
    /bin/sh: leap_gen_top: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input 3D structure PDB file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/structure.pdb). Accepted formats: PDB
* **input_lib_path** (*string*): Input ligand library parameters file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/ligand.lib). Accepted formats: LIB
* **input_frcmod_path** (*string*): Input ligand frcmod parameters file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/ligand.frcmod). Accepted formats: FRCMOD
* **input_params_path** (*string*): Additional leap parameter files to load with loadAmberParams Leap command. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/frcmod.ionsdang_spce). Accepted formats: IN, LEAPIN, TXT, ZIP
* **input_source_path** (*string*): Additional leap command files to load with source Leap command. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/leaprc.water.spce). Accepted formats: IN, LEAPIN, TXT, ZIP
* **output_pdb_path** (*string*): Output 3D structure PDB file matching the topology file. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.leap.pdb). Accepted formats: PDB
* **output_top_path** (*string*): Output topology file (AMBER ParmTop). File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.leap.top). Accepted formats: TOP, PARMTOP, PRMTOP
* **output_crd_path** (*string*): Output coordinates file (AMBER crd). File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.leap.crd). Accepted formats: CRD, MDCRD, INPCRD
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **forcefield** (*array*): ([protein.ff14SB,DNA.bsc1,gaff]) Forcefield to be used for the structure generation. .
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_leap_gen_top.yml)
```python
properties:
  forcefield:
  - protein.ff14SB
  remove_tmp: true

```
#### Command line
```python
leap_gen_top --config config_leap_gen_top.yml --input_pdb_path structure.pdb --input_lib_path ligand.lib --input_frcmod_path ligand.frcmod --input_params_path frcmod.ionsdang_spce --input_source_path leaprc.water.spce --output_pdb_path structure.leap.pdb --output_top_path structure.leap.top --output_crd_path structure.leap.crd
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_leap_gen_top.json)
```python
{
  "properties": {
    "forcefield": [
      "protein.ff14SB"
    ],
    "remove_tmp": true
  }
}
```
#### Command line
```python
leap_gen_top --config config_leap_gen_top.json --input_pdb_path structure.pdb --input_lib_path ligand.lib --input_frcmod_path ligand.frcmod --input_params_path frcmod.ionsdang_spce --input_source_path leaprc.water.spce --output_pdb_path structure.leap.pdb --output_top_path structure.leap.top --output_crd_path structure.leap.crd
```

## Pdb4amber
Wrapper of the AmberTools (AMBER MD Package) pdb4amber tool module.
### Get help
Command:
```python
pdb4amber -h
```
    /bin/sh: pdb4amber: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input 3D structure PDB file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pdb4amber/1aki_fixed.pdb). Accepted formats: PDB
* **output_pdb_path** (*string*): Output 3D structure PDB file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/pdb4amber/structure.pdb4amber.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **remove_hydrogens** (*boolean*): (True) Remove hydrogen atoms from the PDB file..
* **remove_waters** (*boolean*): (True) Remove water molecules from the PDB file..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_pdb4amber.yml)
```python
properties:
  remove_tmp: true

```
#### Command line
```python
pdb4amber --config config_pdb4amber.yml --input_pdb_path 1aki_fixed.pdb --output_pdb_path structure.pdb4amber.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_pdb4amber.json)
```python
{
  "properties": {
    "remove_tmp": true
  }
}
```
#### Command line
```python
pdb4amber --config config_pdb4amber.json --input_pdb_path 1aki_fixed.pdb --output_pdb_path structure.pdb4amber.pdb
```

## Parmed_cpinutil
Wrapper of the AmberTools (AMBER MD Package) parmed tool module.
### Get help
Command:
```python
parmed_cpinutil -h
```
    /bin/sh: parmed_cpinutil: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_top_path** (*string*): Input AMBER topology file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/parmed/structure.solv.top). Accepted formats: TOP, PARMTOP, PRMTOP
* **output_cpin_path** (*string*): Output AMBER constant pH input (CPin) file. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/parmed/cln025.cpin). Accepted formats: CPIN
* **output_top_path** (*string*): Output topology file (AMBER ParmTop). File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/parmed/cln025.cpH.prmtop). Accepted formats: TOP, PARMTOP, PRMTOP
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **resnames** (*string*): (None) Residue names to include in CPIN file. .
* **igb** (*integer*): (2) Generalized Born model which you intend to use to evaluate dynamics or protonation state swaps. .
* **system** (*string*): (Unknown) Name of system to titrate..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_parmed_cpinutil.yml)
```python
properties:
  igb: 2
  remove_tmp: true
  resnames: AS4 GL4
  system: cln025

```
#### Command line
```python
parmed_cpinutil --config config_parmed_cpinutil.yml --input_top_path structure.solv.top --output_cpin_path cln025.cpin --output_top_path cln025.cpH.prmtop
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_parmed_cpinutil.json)
```python
{
  "properties": {
    "igb": 2,
    "resnames": "AS4 GL4",
    "system": "cln025",
    "remove_tmp": true
  }
}
```
#### Command line
```python
parmed_cpinutil --config config_parmed_cpinutil.json --input_top_path structure.solv.top --output_cpin_path cln025.cpin --output_top_path cln025.cpH.prmtop
```
