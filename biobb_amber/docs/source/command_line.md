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
    usage: leap_solvate [-h] [--config CONFIG] --input_pdb_path INPUT_PDB_PATH [--input_lib_path INPUT_LIB_PATH] [--input_frcmod_path INPUT_FRCMOD_PATH] [--input_params_path INPUT_PARAMS_PATH] [--input_prep_path INPUT_PREP_PATH] [--input_source_path INPUT_SOURCE_PATH] --output_pdb_path OUTPUT_PDB_PATH --output_top_path OUTPUT_TOP_PATH --output_crd_path OUTPUT_CRD_PATH
    
    Generating and solvating a system box for an AMBER MD system. using tLeap program from AmberTools MD package.
    
    options:
      -h, --help            show this help message and exit
      --config CONFIG       Configuration file
    
    required arguments:
      --input_pdb_path INPUT_PDB_PATH
                            Input 3D structure PDB file. Accepted formats: pdb.
      --input_lib_path INPUT_LIB_PATH
                            Input ligand library parameters file. Accepted formats: lib, zip.
      --input_frcmod_path INPUT_FRCMOD_PATH
                            Input ligand frcmod parameters file. Accepted formats: frcmod, zip.
      --input_params_path INPUT_PARAMS_PATH
                            Additional leap parameter files to load with loadAmberParams Leap command. Accepted formats: leapin, in, txt, zip.
      --input_prep_path INPUT_PREP_PATH
                            Additional leap parameter files to load with loadAmberPrep Leap command. Accepted formats: leapin, in, txt, zip.
      --input_source_path INPUT_SOURCE_PATH
                            Additional leap command files to load with source Leap command. Accepted formats: leapin, in, txt, zip.
      --output_pdb_path OUTPUT_PDB_PATH
                            Output 3D structure PDB file matching the topology file. Accepted formats: pdb.
      --output_top_path OUTPUT_TOP_PATH
                            Output topology file (AMBER ParmTop). Accepted formats: top.
      --output_crd_path OUTPUT_CRD_PATH
                            Output coordinates file (AMBER crd). Accepted formats: crd.
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input 3D structure PDB file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/structure.leap.pdb). Accepted formats: PDB
* **input_lib_path** (*string*): Input ligand library parameters file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/ligand.lib). Accepted formats: LIB, ZIP
* **input_frcmod_path** (*string*): Input ligand frcmod parameters file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/ligand.frcmod). Accepted formats: FRCMOD, ZIP
* **input_params_path** (*string*): Additional leap parameter files to load with loadAmberParams Leap command. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/frcmod.ionsdang_spce.txt). Accepted formats: IN, LEAPIN, TXT, ZIP
* **input_prep_path** (*string*): Additional leap parameter files to load with loadAmberPrep Leap command. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/heme_all.in). Accepted formats: IN, LEAPIN, TXT, ZIP
* **input_source_path** (*string*): Additional leap command files to load with source Leap command. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/leaprc.water.spce.txt). Accepted formats: IN, LEAPIN, TXT, ZIP
* **output_pdb_path** (*string*): Output 3D structure PDB file matching the topology file. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.solv.pdb). Accepted formats: PDB
* **output_top_path** (*string*): Output topology file (AMBER ParmTop). File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.solv.top). Accepted formats: TOP, PARMTOP, PRMTOP
* **output_crd_path** (*string*): Output coordinates file (AMBER crd). File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.solv.crd). Accepted formats: CRD, MDCRD, INPCRD
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **forcefield** (*array*): ([protein.ff14SB,DNA.bsc1,gaff]) Forcefields to be used for the structure generation. Each item should be either a path to a leaprc file or a string with the leaprc file name if the force field is included with Amber (e.g. "/path/to/leaprc.protein.ff14SB" or "protein.ff14SB"). Default values: ["protein.ff14SB","DNA.bsc1","gaff"]..
* **water_type** (*string*): (TIP3PBOX) Water molecule parameters to be used for the topology. .
* **box_type** (*string*): (truncated_octahedron) Type for the MD system box. .
* **ions_type** (*string*): (ionsjc_tip3p) Ions type. .
* **neutralise** (*boolean*): (False) Energetically neutralise the system adding the necessary counterions..
* **iso** (*boolean*): (False) Make the box isometric..
* **positive_ions_number** (*integer*): (0) Number of additional positive ions to include in the system box..
* **negative_ions_number** (*integer*): (0) Number of additional negative ions to include in the system box..
* **positive_ions_type** (*string*): (Na+) Type of additional positive ions to include in the system box. .
* **negative_ions_type** (*string*): (Cl-) Type of additional negative ions to include in the system box. .
* **distance_to_molecule** (*number*): (8.0) Size for the MD system box -in Angstroms-, defined such as the minimum distance between any atom originally present in solute and the edge of the periodic box is given by this distance parameter..
* **closeness** (*number*): (1.0) How close, in Å, solvent ATOMs may come to solute ATOMs..
* **binary_path** (*string*): (tleap) Path to the tleap executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
* **container_path** (*string*): (None) Container path definition..
* **container_image** (*string*): (afandiadib/ambertools:serial) Container image definition..
* **container_volume_path** (*string*): (/tmp) Container volume path definition..
* **container_working_dir** (*string*): (None) Container working directory definition..
* **container_user_id** (*string*): (None) Container user_id definition..
* **container_shell_path** (*string*): (/bin/bash) Path to default shell inside the container..
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
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_leap_solvate_docker.yml)
```python
properties:
  box_type: truncated_octahedron
  container_image: afandiadib/ambertools:serial
  container_path: docker
  container_volume_path: /tmp
  distance_to_molecule: '9.0'
  forcefield:
  - protein.ff14SB
  water_type: TIP3PBOX

```
#### Command line
```python
leap_solvate --config config_leap_solvate.yml --input_pdb_path structure.leap.pdb --input_lib_path ligand.lib --input_frcmod_path ligand.frcmod --input_params_path frcmod.ionsdang_spce.txt --input_prep_path heme_all.in --input_source_path leaprc.water.spce.txt --output_pdb_path structure.solv.pdb --output_top_path structure.solv.top --output_crd_path structure.solv.crd
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
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_leap_solvate_docker.json)
```python
{
  "properties": {
    "forcefield": [
      "protein.ff14SB"
    ],
    "water_type": "TIP3PBOX",
    "distance_to_molecule": "9.0",
    "box_type": "truncated_octahedron",
    "container_path": "docker",
    "container_image": "afandiadib/ambertools:serial",
    "container_volume_path": "/tmp"
  }
}
```
#### Command line
```python
leap_solvate --config config_leap_solvate.json --input_pdb_path structure.leap.pdb --input_lib_path ligand.lib --input_frcmod_path ligand.frcmod --input_params_path frcmod.ionsdang_spce.txt --input_prep_path heme_all.in --input_source_path leaprc.water.spce.txt --output_pdb_path structure.solv.pdb --output_top_path structure.solv.top --output_crd_path structure.solv.crd
```

## Sander_mdrun
Wrapper of the AmberTools (AMBER MD Package) sander tool module.
### Get help
Command:
```python
sander_mdrun -h
```
    usage: sander_mdrun [-h] [--config CONFIG] --input_top_path INPUT_TOP_PATH --input_crd_path INPUT_CRD_PATH [--input_mdin_path INPUT_MDIN_PATH] [--input_cpin_path INPUT_CPIN_PATH] [--input_ref_path INPUT_REF_PATH] --output_log_path OUTPUT_LOG_PATH --output_traj_path OUTPUT_TRAJ_PATH --output_rst_path OUTPUT_RST_PATH [--output_cpout_path OUTPUT_CPOUT_PATH] [--output_cprst_path OUTPUT_CPRST_PATH] [--output_mdinfo_path OUTPUT_MDINFO_PATH]
    
    Running energy minimization, molecular dynamics, and NMR refinements using sander tool from the AmberTools MD package.
    
    options:
      -h, --help            show this help message and exit
      --config CONFIG       Configuration file
      --input_mdin_path INPUT_MDIN_PATH
                            Input configuration file (MD run options) (AMBER mdin). Accepted formats: mdin, in, txt.
      --input_cpin_path INPUT_CPIN_PATH
                            Input constant pH file (AMBER cpin). Accepted formats: cpin.
      --input_ref_path INPUT_REF_PATH
                            Input reference coordinates for position restraints. Accepted formats: rst, rst7.
      --output_cpout_path OUTPUT_CPOUT_PATH
                            Output constant pH file (AMBER cpout). Accepted formats: cpout.
      --output_cprst_path OUTPUT_CPRST_PATH
                            Output constant pH restart file (AMBER rstout). Accepted formats: cprst.
      --output_mdinfo_path OUTPUT_MDINFO_PATH
                            Output MD info. Accepted formats: mdinfo.
    
    required arguments:
      --input_top_path INPUT_TOP_PATH
                            Input topology file (AMBER ParmTop). Accepted formats: top, prmtop, parmtop.
      --input_crd_path INPUT_CRD_PATH
                            Input coordinates file (AMBER crd). Accepted formats: crd, mdcrd.
      --output_log_path OUTPUT_LOG_PATH
                            Output log file. Accepted formats: log, out, txt.
      --output_traj_path OUTPUT_TRAJ_PATH
                            Output trajectory file. Accepted formats: trj, crd, mdcrd, x.
      --output_rst_path OUTPUT_RST_PATH
                            Output restart file. Accepted formats: rst, rst7.
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_top_path** (*string*): Input topology file (AMBER ParmTop). File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/sander/cln025.prmtop). Accepted formats: TOP, PARMTOP, PRMTOP
* **input_crd_path** (*string*): Input coordinates file (AMBER crd). File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/sander/cln025.inpcrd). Accepted formats: CRD, MDCRD, INPCRD, NETCDF, NC, NCRST, RST
* **input_mdin_path** (*string*): Input configuration file (MD run options) (AMBER mdin). File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/sander/npt.mdin). Accepted formats: MDIN, IN, TXT
* **input_cpin_path** (*string*): Input constant pH file (AMBER cpin). File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/sander/cln025.cpin). Accepted formats: CPIN
* **input_ref_path** (*string*): Input reference coordinates for position restraints. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/sander/sander.rst). Accepted formats: RST, RST7, NETCDF, NC, NCRST, CRD
* **output_log_path** (*string*): Output log file. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/sander/sander.log). Accepted formats: LOG, OUT, TXT, O
* **output_traj_path** (*string*): Output trajectory file. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/sander/sander.x). Accepted formats: TRJ, CRD, MDCRD, X, NETCDF, NC
* **output_rst_path** (*string*): Output restart file. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/sander/sander.rst). Accepted formats: RST, RST7, NETCDF, NC, NCRST
* **output_cpout_path** (*string*): Output constant pH file (AMBER cpout). File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/sander/sander.cpout). Accepted formats: CPOUT
* **output_cprst_path** (*string*): Output constant pH restart file (AMBER rstout). File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/sander/sander.cprst). Accepted formats: CPRST, RST, RST7
* **output_mdinfo_path** (*string*): Output MD info. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/sander/sander.mdinfo). Accepted formats: MDINFO
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **mdin** (*object*): ({}) Sander MD run options specification. (Used if *input_mdin_path* is None).
* **simulation_type** (*string*): (minimization) Default options for the mdin file. Each creates a different mdin file. .
* **binary_path** (*string*): (sander) sander binary path to be used..
* **direct_mdin** (*boolean*): (False) Use input_mdin_path as it is, skip file parsing..
* **mpi_bin** (*string*): (None) Path to the MPI runner. Usually "mpirun" or "srun"..
* **mpi_np** (*integer*): (0) Number of MPI processes. Usually an integer bigger than 1..
* **mpi_flags** (*string*): (None) Path to the MPI hostlist file..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
* **container_path** (*string*): (None) Container path definition..
* **container_image** (*string*): (afandiadib/ambertools:serial) Container image definition..
* **container_volume_path** (*string*): (/tmp) Container volume path definition..
* **container_working_dir** (*string*): (None) Container working directory definition..
* **container_user_id** (*string*): (None) Container user_id definition..
* **container_shell_path** (*string*): (/bin/bash) Path to default shell inside the container..
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
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_sander_mdrun_docker.yml)
```python
properties:
  container_image: afandiadib/ambertools:serial
  container_path: docker
  container_volume_path: /tmp
  mdin:
    ioutfm: 0
    maxcyc: 500
    ntwx: 100
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
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_sander_mdrun_docker.json)
```python
{
  "properties": {
    "simulation_type": "minimization",
    "mdin": {
      "maxcyc": 500,
      "ntwx": 100,
      "ioutfm": 0
    },
    "container_path": "docker",
    "container_image": "afandiadib/ambertools:serial",
    "container_volume_path": "/tmp"
  }
}
```
#### Command line
```python
sander_mdrun --config config_sander_mdrun.json --input_top_path cln025.prmtop --input_crd_path cln025.inpcrd --input_mdin_path npt.mdin --input_cpin_path cln025.cpin --input_ref_path sander.rst --output_log_path sander.log --output_traj_path sander.x --output_rst_path sander.rst --output_cpout_path sander.cpout --output_cprst_path sander.cprst --output_mdinfo_path sander.mdinfo
```

## Cestats_run
Wrapper of the AmberTools (AMBER MD Package) cestats tool module.
### Get help
Command:
```python
cestats_run -h
```
    usage: cestats_run [-h] [--config CONFIG] --input_cein_path INPUT_CEIN_PATH --input_ceout_path INPUT_CEOUT_PATH --output_dat_path OUTPUT_DAT_PATH [--output_population_path OUTPUT_POPULATION_PATH] [--output_chunk_path OUTPUT_CHUNK_PATH] [--output_cumulative_path OUTPUT_CUMULATIVE_PATH] [--output_conditional_path OUTPUT_CONDITIONAL_PATH] [--output_chunk_conditional_path OUTPUT_CHUNK_CONDITIONAL_PATH]
    
    Analyzing the results of constant Redox potential MD simulations using cestats tool from the AMBER MD package.
    
    options:
      -h, --help            show this help message and exit
      --config CONFIG       Configuration file
    
    required arguments:
      --input_cein_path INPUT_CEIN_PATH
                            Input cein or cpein file (from pmemd or sander) with titrating residue information. Accepted formats: cein, cpein.
      --input_ceout_path INPUT_CEOUT_PATH
                            Output ceout file (AMBER ceout). Accepted formats: ceout.
      --output_dat_path OUTPUT_DAT_PATH
                            Output file to which the standard calceo-type statistics are written. Accepted formats: dat, out, txt, o.
      --output_population_path OUTPUT_POPULATION_PATH
                            Output file where protonation state populations are printed for every state of every residue. Accepted formats: dat, out, txt, o.
      --output_chunk_path OUTPUT_CHUNK_PATH
                            Output file where the time series data calculated over chunks of the simulation are printed. Accepted formats: dat, out, txt, o.
      --output_cumulative_path OUTPUT_CUMULATIVE_PATH
                            Output file where the cumulative time series data is printed. Accepted formats: dat, out, txt, o.
      --output_conditional_path OUTPUT_CONDITIONAL_PATH
                            Output file with requested conditional probabilities. Accepted formats: dat, out, txt, o.
      --output_chunk_conditional_path OUTPUT_CHUNK_CONDITIONAL_PATH
                            Output file with a time series of the conditional probabilities over a trajectory split up into chunks. Accepted formats: dat, out, txt, o.
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_cein_path** (*string*): Input cein or cpein file (from pmemd or sander) with titrating residue information. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/cphstats/structure.cein). Accepted formats: CEIN, CPEIN
* **input_ceout_path** (*string*): Output ceout file (AMBER ceout). File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/cphstats/sander.ceout.gz). Accepted formats: CEOUT, ZIP, GZIP, GZ
* **output_dat_path** (*string*): Output file to which the standard calceo-type statistics are written. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/cphstats/cestats.dat). Accepted formats: DAT, OUT, TXT, O
* **output_population_path** (*string*): Output file where protonation state populations are printed for every state of every residue. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/cphstats/cestats.dat). Accepted formats: DAT, OUT, TXT, O
* **output_chunk_path** (*string*): Output file where the time series data calculated over chunks of the simulation are printed. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/cphstats/cestats.dat). Accepted formats: DAT, OUT, TXT, O
* **output_cumulative_path** (*string*): Output file where the cumulative time series data is printed. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/cphstats/cestats.dat). Accepted formats: DAT, OUT, TXT, O
* **output_conditional_path** (*string*): Output file with requested conditional probabilities. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/cphstats/cestats.dat). Accepted formats: DAT, OUT, TXT, O
* **output_chunk_conditional_path** (*string*): Output file with a time series of the conditional probabilities over a trajectory split up into chunks. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/cphstats/cestats.dat). Accepted formats: DAT, OUT, TXT, O
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **timestep** (*number*): (0.002) Simulation time step -in ps-, used to print data as a function of time..
* **verbose** (*boolean*): (False) Controls how much information is printed to the calceo-style output file. Options are: False - Just print fraction protonated. True - Print everything calceo prints..
* **interval** (*integer*): (1000) Interval between which to print out time series data like chunks, cumulative data, and running averages. It is also used as the window of the conditional probability time series..
* **reduced** (*boolean*): (True) Print out reduction fraction instead of oxidation fraction in time series data..
* **eos** (*boolean*): (False) Print predicted Eos -via Nernst equation- in place of fraction reduced or oxidized..
* **calceo** (*boolean*): (True) Triggers the calceo-style output..
* **running_avg_window** (*integer*): (100) Defines a window size -in MD steps- for a moving, running average time series..
* **chunk_window** (*integer*): (100) Computes the time series data over a chunk of the simulation of this specified size -window- time steps..
* **cumulative** (*boolean*): (False) Computes the cumulative average time series data over the course of the trajectory..
* **fix_remd** (*string*): () This option will trigger cestats to reassemble the titration data into pH-specific ensembles. This is an exclusive mode of the program, no other analyses will be done..
* **conditional** (*string*): () Evaluates conditional probabilities. CONDITIONAL should be a string of the format: <resid>:<state>,<resid>:<state>,... or <resid>:PROT,<resid>:DEPROT,... or <resid>:<state1>;<state2>,<resid>:PROT,... where <resid> is the residue number in the prmtop and <state> is either the state number or -p-rotonated or -d-eprotonated, case-insensitive..
* **binary_path** (*string*): (cestats) Path to the cestats executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
* **container_path** (*string*): (None) Container path definition..
* **container_image** (*string*): (afandiadib/ambertools:serial) Container image definition..
* **container_volume_path** (*string*): (/tmp) Container volume path definition..
* **container_working_dir** (*string*): (None) Container working directory definition..
* **container_user_id** (*string*): (None) Container user_id definition..
* **container_shell_path** (*string*): (/bin/bash) Path to default shell inside the container..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_cestats_run.yml)
```python
properties:
  remove_tmp: true

```
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_cestats_run_docker.yml)
```python
properties:
  container_image: afandiadib/ambertools:serial
  container_path: docker
  container_volume_path: /tmp

```
#### Command line
```python
cestats_run --config config_cestats_run.yml --input_cein_path structure.cein --input_ceout_path sander.ceout.gz --output_dat_path cestats.dat --output_population_path cestats.dat --output_chunk_path cestats.dat --output_cumulative_path cestats.dat --output_conditional_path cestats.dat --output_chunk_conditional_path cestats.dat
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_cestats_run.json)
```python
{
  "properties": {
    "remove_tmp": true
  }
}
```
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_cestats_run_docker.json)
```python
{
  "properties": {
    "container_path": "docker",
    "container_image": "afandiadib/ambertools:serial",
    "container_volume_path": "/tmp"
  }
}
```
#### Command line
```python
cestats_run --config config_cestats_run.json --input_cein_path structure.cein --input_ceout_path sander.ceout.gz --output_dat_path cestats.dat --output_population_path cestats.dat --output_chunk_path cestats.dat --output_cumulative_path cestats.dat --output_conditional_path cestats.dat --output_chunk_conditional_path cestats.dat
```

## Pmemd_mdrun
Wrapper of the AmberTools (AMBER MD Package) pmemd tool module.
### Get help
Command:
```python
pmemd_mdrun -h
```
    usage: pmemd_mdrun [-h] [--config CONFIG] --input_top_path INPUT_TOP_PATH --input_crd_path INPUT_CRD_PATH [--input_mdin_path INPUT_MDIN_PATH] [--input_cpin_path INPUT_CPIN_PATH] [--input_ref_path INPUT_REF_PATH] --output_log_path OUTPUT_LOG_PATH --output_traj_path OUTPUT_TRAJ_PATH --output_rst_path OUTPUT_RST_PATH [--output_cpout_path OUTPUT_CPOUT_PATH] [--output_cprst_path OUTPUT_CPRST_PATH] [--output_mdinfo_path OUTPUT_MDINFO_PATH]
    
    Running molecular dynamics using pmemd tool from the AMBER MD package.
    
    options:
      -h, --help            show this help message and exit
      --config CONFIG       Configuration file
    
    required arguments:
      --input_top_path INPUT_TOP_PATH
                            Input topology file (AMBER ParmTop). Accepted formats: top, prmtop, parmtop.
      --input_crd_path INPUT_CRD_PATH
                            Input coordinates file (AMBER crd). Accepted formats: crd, mdcrd.
      --input_mdin_path INPUT_MDIN_PATH
                            Input configuration file (MD run options) (AMBER mdin). Accepted formats: mdin, in, txt.
      --input_cpin_path INPUT_CPIN_PATH
                            Input constant pH file (AMBER cpin). Accepted formats: cpin.
      --input_ref_path INPUT_REF_PATH
                            Input reference coordinates for position restraints. Accepted formats: rst, rst7.
      --output_log_path OUTPUT_LOG_PATH
                            Output log file. Accepted formats: log, out, txt.
      --output_traj_path OUTPUT_TRAJ_PATH
                            Output trajectory file. Accepted formats: trj, crd, mdcrd, x.
      --output_rst_path OUTPUT_RST_PATH
                            Output restart file. Accepted formats: rst, rst7.
      --output_cpout_path OUTPUT_CPOUT_PATH
                            Output constant pH file (AMBER cpout). Accepted formats: cpout.
      --output_cprst_path OUTPUT_CPRST_PATH
                            Output constant pH restart file (AMBER rstout). Accepted formats: cprst.
      --output_mdinfo_path OUTPUT_MDINFO_PATH
                            Output MD info. Accepted formats: mdinfo.
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_top_path** (*string*): Input topology file (AMBER ParmTop). File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pmemd/cln025.prmtop). Accepted formats: TOP, PARMTOP, PRMTOP
* **input_crd_path** (*string*): Input coordinates file (AMBER crd). File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pmemd/cln025.inpcrd). Accepted formats: CRD, MDCRD, INPCRD, RST, RST7, NETCDF, NC, NCRST
* **input_mdin_path** (*string*): Input configuration file (MD run options) (AMBER mdin). File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pmemd/npt.mdin). Accepted formats: MDIN, IN, TXT
* **input_cpin_path** (*string*): Input constant pH file (AMBER cpin). File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pmemd/cln025.cpin). Accepted formats: CPIN
* **input_ref_path** (*string*): Input reference coordinates for position restraints. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pmemd/sander.rst). Accepted formats: CRD, MDCRD, INPCRD, RST, RST7, NETCDF, NC, NCRST
* **output_log_path** (*string*): Output log file. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/pmemd/sander.log). Accepted formats: LOG, OUT, TXT, O
* **output_traj_path** (*string*): Output trajectory file. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/pmemd/sander.x). Accepted formats: TRJ, CRD, MDCRD, X, NETCDF, NC
* **output_rst_path** (*string*): Output restart file. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/pmemd/sander.rst). Accepted formats: RST, RST7, NETCDF, NC, NCRST
* **output_cpout_path** (*string*): Output constant pH file (AMBER cpout). File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/pmemd/sander.cpout). Accepted formats: CPOUT
* **output_cprst_path** (*string*): Output constant pH restart file (AMBER rstout). File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/pmemd/sander.cprst). Accepted formats: CPRST, RST, RST7
* **output_mdinfo_path** (*string*): Output MD info. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/pmemd/sander.mdinfo). Accepted formats: MDINFO
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **mdin** (*object*): ({}) pmemd MD run options specification. (Used if *input_mdin_path* is None).
* **binary_path** (*string*): (pmemd) pmemd binary path to be used..
* **simulation_type** (*string*): (minimization) Default options for the mdin file. Each creates a different mdin file. .
* **mpi_bin** (*string*): (None) Path to the MPI runner. Usually "mpirun" or "srun"..
* **mpi_np** (*integer*): (0) Number of MPI processes. Usually an integer bigger than 1..
* **mpi_flags** (*string*): (None) Path to the MPI hostlist file..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
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

## Pdb4amber_run
Wrapper of the AmberTools (AMBER MD Package) pdb4amber tool module.
### Get help
Command:
```python
pdb4amber_run -h
```
    usage: pdb4amber_run [-h] [--config CONFIG] --input_pdb_path INPUT_PDB_PATH --output_pdb_path OUTPUT_PDB_PATH
    
    Analyse PDB files and clean them for further usage, especially with the LEaP programs of Amber, using pdb4amber tool from the AmberTools MD package.
    
    options:
      -h, --help            show this help message and exit
      --config CONFIG       Configuration file
    
    required arguments:
      --input_pdb_path INPUT_PDB_PATH
                            Input 3D structure PDB file. Accepted formats: pdb.
      --output_pdb_path OUTPUT_PDB_PATH
                            Output 3D structure PDB file. Accepted formats: pdb.
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input 3D structure PDB file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pdb4amber/1aki_fixed.pdb). Accepted formats: PDB
* **output_pdb_path** (*string*): Output 3D structure PDB file. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/pdb4amber/structure.pdb4amber.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **remove_hydrogens** (*boolean*): (False) Remove hydrogen atoms from the PDB file..
* **remove_waters** (*boolean*): (False) Remove water molecules from the PDB file..
* **constant_pH** (*boolean*): (False) Rename ionizable residues e.g. GLU,ASP,HIS for constant pH simulation..
* **reduce** (*boolean*): (False) Run Reduce first to add hydrogen atoms..
* **binary_path** (*string*): (pdb4amber) Path to the pdb4amber executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
* **container_path** (*string*): (None) Container path definition..
* **container_image** (*string*): (afandiadib/ambertools:serial) Container image definition..
* **container_volume_path** (*string*): (/tmp) Container volume path definition..
* **container_working_dir** (*string*): (None) Container working directory definition..
* **container_user_id** (*string*): (None) Container user_id definition..
* **container_shell_path** (*string*): (/bin/bash) Path to default shell inside the container..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_pdb4amber_run.yml)
```python
properties:
  remove_tmp: true

```
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_pdb4amber_run_docker.yml)
```python
properties:
  container_image: afandiadib/ambertools:serial
  container_path: docker
  container_volume_path: /tmp

```
#### Command line
```python
pdb4amber_run --config config_pdb4amber_run.yml --input_pdb_path 1aki_fixed.pdb --output_pdb_path structure.pdb4amber.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_pdb4amber_run.json)
```python
{
  "properties": {
    "remove_tmp": true
  }
}
```
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_pdb4amber_run_docker.json)
```python
{
  "properties": {
    "container_path": "docker",
    "container_image": "afandiadib/ambertools:serial",
    "container_volume_path": "/tmp"
  }
}
```
#### Command line
```python
pdb4amber_run --config config_pdb4amber_run.json --input_pdb_path 1aki_fixed.pdb --output_pdb_path structure.pdb4amber.pdb
```

## Process_mdout
Wrapper of the AmberTools (AMBER MD Package) process_mdout tool module.
### Get help
Command:
```python
process_mdout -h
```
    usage: process_mdout [-h] [--config CONFIG] --input_log_path INPUT_LOG_PATH --output_dat_path OUTPUT_DAT_PATH
    
    Parses the AMBER (sander) MD output file (log) and dumps statistics that can then be plotted. Using the process_mdout.pl tool from the AmberTools MD package.
    
    options:
      -h, --help            show this help message and exit
      --config CONFIG       Configuration file
    
    required arguments:
      --input_log_path INPUT_LOG_PATH
                            AMBER (sander) MD output (log) file. Accepted formats: log, out, txt, o.
      --output_dat_path OUTPUT_DAT_PATH
                            Dat output file containing data from the specified terms along the MD process. File type: output. Accepted formats: dat, txt, csv.
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_log_path** (*string*): AMBER (sander) MD output (log) file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/process/sander.heat.log). Accepted formats: LOG, OUT, TXT, O
* **output_dat_path** (*string*): Dat output file containing data from the specified terms along the minimization process. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/process/sander.md.temp.dat). Accepted formats: DAT, TXT, CSV
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **terms** (*array*): ([ETOT]) Statistics descriptors. .
* **binary_path** (*string*): (process_mdout.perl) Path to the process_mdout.perl executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
* **container_path** (*string*): (None) Container path definition..
* **container_image** (*string*): (afandiadib/ambertools:serial) Container image definition..
* **container_volume_path** (*string*): (/tmp) Container volume path definition..
* **container_working_dir** (*string*): (None) Container working directory definition..
* **container_user_id** (*string*): (None) Container user_id definition..
* **container_shell_path** (*string*): (/bin/bash) Path to default shell inside the container..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_process_mdout.yml)
```python
properties:
  remove_tmp: true
  terms:
  - TEMP
  - VOLUME
  - EKTOT

```
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_process_mdout_docker.yml)
```python
properties:
  container_image: afandiadib/ambertools:serial
  container_path: docker
  container_volume_path: /tmp
  container_working_dir: /tmp
  terms:
  - TEMP
  - VOLUME
  - EKTOT

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
      "TEMP",
      "VOLUME",
      "EKTOT"
    ],
    "remove_tmp": true
  }
}
```
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_process_mdout_docker.json)
```python
{
  "properties": {
    "terms": [
      "TEMP",
      "VOLUME",
      "EKTOT"
    ],
    "container_path": "docker",
    "container_image": "afandiadib/ambertools:serial",
    "container_volume_path": "/tmp",
    "container_working_dir": "/tmp"
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
    usage: leap_add_ions [-h] [--config CONFIG] --input_pdb_path INPUT_PDB_PATH [--input_lib_path INPUT_LIB_PATH] [--input_frcmod_path INPUT_FRCMOD_PATH] [--input_params_path INPUT_PARAMS_PATH] [--input_prep_path INPUT_PREP_PATH] [--input_source_path INPUT_SOURCE_PATH] --output_pdb_path OUTPUT_PDB_PATH --output_top_path OUTPUT_TOP_PATH --output_crd_path OUTPUT_CRD_PATH
    
    Adds counterions to a system box for an AMBER MD system using tLeap.
    
    options:
      -h, --help            show this help message and exit
      --config CONFIG       Configuration file
    
    required arguments:
      --input_pdb_path INPUT_PDB_PATH
                            Input 3D structure PDB file. Accepted formats: pdb.
      --input_lib_path INPUT_LIB_PATH
                            Input ligand library parameters file. Accepted formats: lib, zip.
      --input_frcmod_path INPUT_FRCMOD_PATH
                            Input ligand frcmod parameters file. Accepted formats: frcmod, zip.
      --input_params_path INPUT_PARAMS_PATH
                            Additional leap parameter files to load with loadAmberParams Leap command. Accepted formats: leapin, in, txt, zip.
      --input_prep_path INPUT_PREP_PATH
                            Additional leap parameter files to load with loadAmberPrep Leap command. Accepted formats: leapin, in, txt, zip.
      --input_source_path INPUT_SOURCE_PATH
                            Additional leap command files to load with source Leap command. Accepted formats: leapin, in, txt, zip.
      --output_pdb_path OUTPUT_PDB_PATH
                            Output 3D structure PDB file matching the topology file. Accepted formats: pdb.
      --output_top_path OUTPUT_TOP_PATH
                            Output topology file (AMBER ParmTop). Accepted formats: top.
      --output_crd_path OUTPUT_CRD_PATH
                            Output coordinates file (AMBER crd). Accepted formats: crd.
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input 3D structure PDB file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/structure.solv.pdb). Accepted formats: PDB
* **input_lib_path** (*string*): Input ligand library parameters file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/ligand.lib). Accepted formats: LIB, ZIP
* **input_frcmod_path** (*string*): Input ligand frcmod parameters file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/ligand.frcmod). Accepted formats: FRCMOD, ZIP
* **input_params_path** (*string*): Additional leap parameter files to load with loadAmberParams Leap command. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/frcmod.ionsdang_spce.txt). Accepted formats: IN, LEAPIN, TXT, ZIP
* **input_prep_path** (*string*): Additional leap parameter files to load with loadAmberPrep Leap command. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/frcmod.ionsdang_spce.txt). Accepted formats: IN, LEAPIN, TXT, ZIP
* **input_source_path** (*string*): Additional leap command files to load with source Leap command. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/leaprc.water.spce.txt). Accepted formats: IN, LEAPIN, TXT, ZIP
* **output_pdb_path** (*string*): Output 3D structure PDB file matching the topology file. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.ions.pdb). Accepted formats: PDB
* **output_top_path** (*string*): Output topology file (AMBER ParmTop). File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.ions.top). Accepted formats: TOP, PARMTOP, PRMTOP
* **output_crd_path** (*string*): Output coordinates file (AMBER crd). File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.ions.crd). Accepted formats: CRD, MDCRD, INPCRD
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **forcefield** (*array*): ([protein.ff14SB,DNA.bsc1,gaff]) Forcefields to be used for the structure generation. Each item should be either a path to a leaprc file or a string with the leaprc file name if the force field is included with Amber (e.g. "/path/to/leaprc.protein.ff14SB" or "protein.ff14SB"). Default values: ["protein.ff14SB","DNA.bsc1","gaff"]..
* **water_type** (*string*): (TIP3PBOX) Water molecule parameters to be used for the topology. .
* **box_type** (*string*): (truncated_octahedron) Type for the MD system box. .
* **ions_type** (*string*): (ionsjc_tip3p) Ions type. .
* **neutralise** (*boolean*): (True) Energetically neutralise the system adding the necessary counterions..
* **ionic_concentration** (*number*): (50.0) Additional ionic concentration to include in the system box. Units in Mol/L..
* **positive_ions_number** (*integer*): (0) Number of additional positive ions to include in the system box..
* **negative_ions_number** (*integer*): (0) Number of additional negative ions to include in the system box..
* **positive_ions_type** (*string*): (Na+) Type of additional positive ions to include in the system box. .
* **negative_ions_type** (*string*): (Cl-) Type of additional negative ions to include in the system box. .
* **binary_path** (*string*): (tleap) Path to the tleap executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
* **container_path** (*string*): (None) Container path definition..
* **container_image** (*string*): (afandiadib/ambertools:serial) Container image definition..
* **container_volume_path** (*string*): (/tmp) Container volume path definition..
* **container_working_dir** (*string*): (None) Container working directory definition..
* **container_user_id** (*string*): (None) Container user_id definition..
* **container_shell_path** (*string*): (/bin/bash) Path to default shell inside the container..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_leap_add_ions.yml)
```python
properties:
  box_type: truncated_octahedron
  forcefield:
  - DNA.bsc1
  ionic_concentration: 100
  ions_type: ionsjc_tip4pew
  positive_ions_type: K+
  water_type: OPCBOX

```
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_leap_add_ions_docker.yml)
```python
properties:
  box_type: truncated_octahedron
  container_image: afandiadib/ambertools:serial
  container_path: docker
  container_volume_path: /tmp
  forcefield:
  - DNA.bsc1
  ionic_concentration: 100
  ions_type: ionsjc_tip4pew
  positive_ions_type: K+
  water_type: OPCBOX

```
#### Command line
```python
leap_add_ions --config config_leap_add_ions.yml --input_pdb_path structure.solv.pdb --input_lib_path ligand.lib --input_frcmod_path ligand.frcmod --input_params_path frcmod.ionsdang_spce.txt --input_prep_path frcmod.ionsdang_spce.txt --input_source_path leaprc.water.spce.txt --output_pdb_path structure.ions.pdb --output_top_path structure.ions.top --output_crd_path structure.ions.crd
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_leap_add_ions.json)
```python
{
  "properties": {
    "forcefield": [
      "DNA.bsc1"
    ],
    "water_type": "OPCBOX",
    "ions_type": "ionsjc_tip4pew",
    "box_type": "truncated_octahedron",
    "ionic_concentration": 100,
    "positive_ions_type": "K+"
  }
}
```
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_leap_add_ions_docker.json)
```python
{
  "properties": {
    "forcefield": [
      "DNA.bsc1"
    ],
    "water_type": "OPCBOX",
    "ions_type": "ionsjc_tip4pew",
    "box_type": "truncated_octahedron",
    "ionic_concentration": 100,
    "positive_ions_type": "K+",
    "container_path": "docker",
    "container_image": "afandiadib/ambertools:serial",
    "container_volume_path": "/tmp"
  }
}
```
#### Command line
```python
leap_add_ions --config config_leap_add_ions.json --input_pdb_path structure.solv.pdb --input_lib_path ligand.lib --input_frcmod_path ligand.frcmod --input_params_path frcmod.ionsdang_spce.txt --input_prep_path frcmod.ionsdang_spce.txt --input_source_path leaprc.water.spce.txt --output_pdb_path structure.ions.pdb --output_top_path structure.ions.top --output_crd_path structure.ions.crd
```

## Cphstats_run
Wrapper of the AmberTools (AMBER MD Package) cphstats tool module.
### Get help
Command:
```python
cphstats_run -h
```
    usage: cphstats_run [-h] [--config CONFIG] --input_cpin_path INPUT_CPIN_PATH --input_cpout_path INPUT_CPOUT_PATH --output_dat_path OUTPUT_DAT_PATH [--output_population_path OUTPUT_POPULATION_PATH] [--output_chunk_path OUTPUT_CHUNK_PATH] [--output_cumulative_path OUTPUT_CUMULATIVE_PATH] [--output_conditional_path OUTPUT_CONDITIONAL_PATH] [--output_chunk_conditional_path OUTPUT_CHUNK_CONDITIONAL_PATH]
    
    Analyzing the results of constant pH MD simulations using cphstats tool from the AMBER MD package.
    
    options:
      -h, --help            show this help message and exit
      --config CONFIG       Configuration file
    
    required arguments:
      --input_cpin_path INPUT_CPIN_PATH
                            Input constant pH file (AMBER cpin). Accepted formats: cpin.
      --input_cpout_path INPUT_CPOUT_PATH
                            Output constant pH file (AMBER cpout). Accepted formats: cpout.
      --output_dat_path OUTPUT_DAT_PATH
                            Output file to which the standard calcpka-type statistics are written. Accepted formats: dat, out, txt, o.
      --output_population_path OUTPUT_POPULATION_PATH
                            Output file where protonation state populations are printed for every state of every residue. Accepted formats: dat, out, txt, o.
      --output_chunk_path OUTPUT_CHUNK_PATH
                            Output file where the time series data calculated over chunks of the simulation are printed. Accepted formats: dat, out, txt, o.
      --output_cumulative_path OUTPUT_CUMULATIVE_PATH
                            Output file where the cumulative time series data is printed. Accepted formats: dat, out, txt, o.
      --output_conditional_path OUTPUT_CONDITIONAL_PATH
                            Output file with requested conditional probabilities. Accepted formats: dat, out, txt, o.
      --output_chunk_conditional_path OUTPUT_CHUNK_CONDITIONAL_PATH
                            Output file with a time series of the conditional probabilities over a trajectory split up into chunks. Accepted formats: dat, out, txt, o.
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_cpin_path** (*string*): Input constant pH file (AMBER cpin). File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/cphstats/structure.cpin). Accepted formats: CPIN
* **input_cpout_path** (*string*): Output constant pH file (AMBER cpout). File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/cphstats/sander.pH.cpout). Accepted formats: CPOUT, ZIP, GZIP
* **output_dat_path** (*string*): Output file to which the standard calcpka-type statistics are written. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/cphstats/cphstats.pH.dat). Accepted formats: DAT, OUT, TXT, O
* **output_population_path** (*string*): Output file where protonation state populations are printed for every state of every residue. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/cphstats/cphstats.pH.pop.dat). Accepted formats: DAT, OUT, TXT, O
* **output_chunk_path** (*string*): Output file where the time series data calculated over chunks of the simulation are printed. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/cphstats/cphstats.pH.dat). Accepted formats: DAT, OUT, TXT, O
* **output_cumulative_path** (*string*): Output file where the cumulative time series data is printed. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/cphstats/cphstats.pH.dat). Accepted formats: DAT, OUT, TXT, O
* **output_conditional_path** (*string*): Output file with requested conditional probabilities. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/cphstats/cphstats.pH.dat). Accepted formats: DAT, OUT, TXT, O
* **output_chunk_conditional_path** (*string*): Output file with a time series of the conditional probabilities over a trajectory split up into chunks. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/cphstats/cphstats.pH.dat). Accepted formats: DAT, OUT, TXT, O
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **timestep** (*number*): (0.002) Simulation time step -in ps-, used to print data as a function of time..
* **verbose** (*boolean*): (False) Controls how much information is printed to the calcpka-style output file. Options are: False - Just print fraction protonated. True - Print everything calcpka prints..
* **interval** (*integer*): (1000) Interval between which to print out time series data like chunks, cumulative data, and running averages. It is also used as the window of the conditional probability time series..
* **protonated** (*boolean*): (True) Print out protonation fraction instead of deprotonation fraction in time series data..
* **pka** (*boolean*): (False) Print predicted pKas -via Henderson-Hasselbalch equation- in place of fraction -de-protonated..
* **calcpka** (*boolean*): (True) Triggers the calcpka-style output..
* **running_avg_window** (*integer*): (100) Defines a window size -in MD steps- for a moving, running average time series..
* **chunk_window** (*integer*): (100) Computes the time series data over a chunk of the simulation of this specified size -window- time steps..
* **cumulative** (*boolean*): (False) Computes the cumulative average time series data over the course of the trajectory..
* **fix_remd** (*string*): () This option will trigger cphstats to reassemble the titration data into pH-specific ensembles. This is an exclusive mode of the program, no other analyses will be done..
* **conditional** (*string*): () Evaluates conditional probabilities. CONDITIONAL should be a string of the format: <resid>:<state>,<resid>:<state>,... or <resid>:PROT,<resid>:DEPROT,... or <resid>:<state1>;<state2>,<resid>:PROT,... where <resid> is the residue number in the prmtop and <state> is either the state number or -p-rotonated or -d-eprotonated, case-insensitive..
* **binary_path** (*string*): (cphstats) Path to the cphstats executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
* **container_path** (*string*): (None) Container path definition..
* **container_image** (*string*): (afandiadib/ambertools:serial) Container image definition..
* **container_volume_path** (*string*): (/tmp) Container volume path definition..
* **container_working_dir** (*string*): (None) Container working directory definition..
* **container_user_id** (*string*): (None) Container user_id definition..
* **container_shell_path** (*string*): (/bin/bash) Path to default shell inside the container..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_cphstats_run.yml)
```python
properties:
  remove_tmp: true

```
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_cphstats_run_docker.yml)
```python
properties:
  container_image: afandiadib/ambertools:serial
  container_path: docker
  container_volume_path: /tmp

```
#### Command line
```python
cphstats_run --config config_cphstats_run.yml --input_cpin_path structure.cpin --input_cpout_path sander.pH.cpout --output_dat_path cphstats.pH.dat --output_population_path cphstats.pH.pop.dat --output_chunk_path cphstats.pH.dat --output_cumulative_path cphstats.pH.dat --output_conditional_path cphstats.pH.dat --output_chunk_conditional_path cphstats.pH.dat
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_cphstats_run.json)
```python
{
  "properties": {
    "remove_tmp": true
  }
}
```
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_cphstats_run_docker.json)
```python
{
  "properties": {
    "container_path": "docker",
    "container_image": "afandiadib/ambertools:serial",
    "container_volume_path": "/tmp"
  }
}
```
#### Command line
```python
cphstats_run --config config_cphstats_run.json --input_cpin_path structure.cpin --input_cpout_path sander.pH.cpout --output_dat_path cphstats.pH.dat --output_population_path cphstats.pH.pop.dat --output_chunk_path cphstats.pH.dat --output_cumulative_path cphstats.pH.dat --output_conditional_path cphstats.pH.dat --output_chunk_conditional_path cphstats.pH.dat
```

## Process_minout
Wrapper of the AmberTools (AMBER MD Package) process_minout tool module.
### Get help
Command:
```python
process_minout -h
```
    usage: process_minout [-h] [--config CONFIG] --input_log_path INPUT_LOG_PATH --output_dat_path OUTPUT_DAT_PATH
    
    Parses the AMBER (sander) minimization output file (log) and dumps statistics that can then be plotted. Using the process_minout.pl tool from the AmberTools MD package.
    
    options:
      -h, --help            show this help message and exit
      --config CONFIG       Configuration file
    
    required arguments:
      --input_log_path INPUT_LOG_PATH
                            AMBER (sander) minimization output (log) file. Accepted formats: log, out, txt, o.
      --output_dat_path OUTPUT_DAT_PATH
                            Dat output file containing data from the specified terms along the minimization process. File type: output. Accepted formats: dat, txt, csv.
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_log_path** (*string*): AMBER (sander) Minimization output (log) file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/process/sander.min.log). Accepted formats: LOG, OUT, TXT, O
* **output_dat_path** (*string*): Dat output file containing data from the specified terms along the minimization process. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/process/sander.min.energy.dat). Accepted formats: DAT, TXT, CSV
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **terms** (*array*): ([ENERGY]) Statistics descriptors. .
* **binary_path** (*string*): (process_minout.perl) Path to the process_minout.perl executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
* **container_path** (*string*): (None) Container path definition..
* **container_image** (*string*): (afandiadib/ambertools:serial) Container image definition..
* **container_volume_path** (*string*): (/tmp) Container volume path definition..
* **container_working_dir** (*string*): (None) Container working directory definition..
* **container_user_id** (*string*): (None) Container user_id definition..
* **container_shell_path** (*string*): (/bin/bash) Path to default shell inside the container..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_process_minout.yml)
```python
properties:
  remove_tmp: true

```
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_process_minout_docker.yml)
```python
properties:
  container_image: afandiadib/ambertools:serial
  container_path: docker
  container_volume_path: /tmp
  container_working_dir: /tmp

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
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_process_minout_docker.json)
```python
{
  "properties": {
    "container_path": "docker",
    "container_image": "afandiadib/ambertools:serial",
    "container_volume_path": "/tmp",
    "container_working_dir": "/tmp"
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
    usage: leap_build_linear_structure [-h] [--config CONFIG] --output_pdb_path OUTPUT_PDB_PATH
    
    Building a linear (unfolded) 3D structure from an AA sequence.
    
    options:
      -h, --help            show this help message and exit
      --config CONFIG       Configuration file
    
    required arguments:
      --output_pdb_path OUTPUT_PDB_PATH
                            Linear (unfolded) 3D structure PDB file. Accepted formats: pdb.
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **output_pdb_path** (*string*): Linear (unfolded) 3D structure PDB file. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **sequence** (*string*): (ALA GLY SER PRO ARG ALA PRO GLY) Aminoacid sequence to convert to a linear 3D structure. Aminoacids should be written in 3-letter code, with a blank space between them..
* **forcefield** (*array*): ([protein.ff14SB,DNA.bsc1,gaff]) Forcefields to be used for the structure generation. Each item should be either a path to a leaprc file or a string with the leaprc file name if the force field is included with Amber (e.g. "/path/to/leaprc.protein.ff14SB" or "protein.ff14SB"). Default values: ["protein.ff14SB","DNA.bsc1","gaff"]..
* **build_library** (*boolean*): (False) Generate AMBER lib file for the structure..
* **binary_path** (*string*): (tleap) Path to the tleap executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
* **container_path** (*string*): (None) Container path definition..
* **container_image** (*string*): (afandiadib/ambertools:serial) Container image definition..
* **container_volume_path** (*string*): (/tmp) Container volume path definition..
* **container_working_dir** (*string*): (None) Container working directory definition..
* **container_user_id** (*string*): (None) Container user_id definition..
* **container_shell_path** (*string*): (/bin/bash) Path to default shell inside the container..
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
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_leap_build_linear_structure_docker.yml)
```python
properties:
  build_library: false
  container_image: afandiadib/ambertools:serial
  container_path: docker
  container_volume_path: /tmp
  forcefield:
  - protein.ff14SB
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
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_leap_build_linear_structure_docker.json)
```python
{
  "properties": {
    "sequence": "ALA PRO SER ARG LYS ASP GLU GLY GLY ALA",
    "build_library": false,
    "forcefield": [
      "protein.ff14SB"
    ],
    "container_path": "docker",
    "container_image": "afandiadib/ambertools:serial",
    "container_volume_path": "/tmp"
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
    usage: nab_build_dna_structure [-h] [--config CONFIG] --output_pdb_path OUTPUT_PDB_PATH
    
    Building a 3D structure from a DNA sequence using nab.
    
    options:
      -h, --help            show this help message and exit
      --config CONFIG       Configuration file
    
    required arguments:
      --output_pdb_path OUTPUT_PDB_PATH
                            Linear (unfolded) 3D structure PDB file. Accepted formats: pdb.
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
* **binary_path** (*string*): (nab) Path to the nab executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
* **container_path** (*string*): (None) Container path definition..
* **container_image** (*string*): (afandiadib/ambertools:serial) Container image definition..
* **container_volume_path** (*string*): (/tmp) Container volume path definition..
* **container_working_dir** (*string*): (None) Container working directory definition..
* **container_user_id** (*string*): (None) Container user_id definition..
* **container_shell_path** (*string*): (/bin/bash) Path to default shell inside the container..
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
    usage: parmed_hmassrepartition [-h] [--config CONFIG] --input_top_path INPUT_TOP_PATH [--output_top_path OUTPUT_TOP_PATH]
    
    Performs a Hydrogen Mass Repartition from an AMBER topology file using parmed tool from the AmberTools MD package.
    
    options:
      -h, --help            show this help message and exit
      --config CONFIG       Configuration file
    
    required arguments:
      --input_top_path INPUT_TOP_PATH
                            Input AMBER topology file. Accepted formats: top, parmtop, prmtop.
      --output_top_path OUTPUT_TOP_PATH
                            Output topology file (AMBER ParmTop). Accepted formats: top, parmtop, prmtop.
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_top_path** (*string*): Input AMBER topology file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/parmed/input.hmass.prmtop). Accepted formats: TOP, PARMTOP, PRMTOP
* **output_top_path** (*string*): Output topology file (AMBER ParmTop). File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/parmed/output.hmass.prmtop). Accepted formats: TOP, PARMTOP, PRMTOP
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **binary_path** (*string*): (parmed) Path to the parmed executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
* **container_path** (*string*): (None) Container path definition..
* **container_image** (*string*): (afandiadib/ambertools:serial) Container image definition..
* **container_volume_path** (*string*): (/tmp) Container volume path definition..
* **container_working_dir** (*string*): (None) Container working directory definition..
* **container_user_id** (*string*): (None) Container user_id definition..
* **container_shell_path** (*string*): (/bin/bash) Path to default shell inside the container..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_parmed_hmassrepartition.yml)
```python
properties:
  remove_tmp: true

```
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_parmed_hmassrepartition_docker.yml)
```python
properties:
  container_image: afandiadib/ambertools:serial
  container_path: docker
  container_volume_path: /tmp

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
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_parmed_hmassrepartition_docker.json)
```python
{
  "properties": {
    "container_path": "docker",
    "container_image": "afandiadib/ambertools:serial",
    "container_volume_path": "/tmp"
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
    usage: cpptraj_randomize_ions [-h] [--config CONFIG] --input_top_path INPUT_TOP_PATH --input_crd_path INPUT_CRD_PATH --output_pdb_path OUTPUT_PDB_PATH --output_crd_path OUTPUT_CRD_PATH
    
    Swap specified ions with randomly selected solvent molecules using cpptraj tool from the AmberTools MD package.
    
    options:
      -h, --help            show this help message and exit
      --config CONFIG       Configuration file
    
    required arguments:
      --input_top_path INPUT_TOP_PATH
                            Input topology file (AMBER ParmTop). Accepted formats: top, parmtop, prmtop.
      --input_crd_path INPUT_CRD_PATH
                            Input coordinates file (AMBER crd). Accepted formats: crd, mdcrd, inpcrd.
      --output_pdb_path OUTPUT_PDB_PATH
                            Structure PDB file with randomized ions. Accepted formats: pdb.
      --output_crd_path OUTPUT_CRD_PATH
                            Structure CRD file with coordinates including randomized ions. Accepted formats: crd, mdcrd, inpcrd.
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
* **binary_path** (*string*): (cpptraj) Path to the cpptraj executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
* **container_path** (*string*): (None) Container path definition..
* **container_image** (*string*): (afandiadib/ambertools:serial) Container image definition..
* **container_volume_path** (*string*): (/tmp) Container volume path definition..
* **container_working_dir** (*string*): (None) Container working directory definition..
* **container_user_id** (*string*): (None) Container user_id definition..
* **container_shell_path** (*string*): (/bin/bash) Path to default shell inside the container..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_cpptraj_randomize_ions.yml)
```python
properties:
  remove_tmp: true

```
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_cpptraj_randomize_ions_docker.yml)
```python
properties:
  container_image: afandiadib/ambertools:serial
  container_path: docker
  container_volume_path: /tmp

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
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_cpptraj_randomize_ions_docker.json)
```python
{
  "properties": {
    "container_path": "docker",
    "container_image": "afandiadib/ambertools:serial",
    "container_volume_path": "/tmp"
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
    usage: amber_to_pdb [-h] [--config CONFIG] --input_top_path INPUT_TOP_PATH --input_crd_path INPUT_CRD_PATH --output_pdb_path OUTPUT_PDB_PATH
    
    Generates a PDB structure from AMBER topology (parmtop) and coordinates (crd) files, using the ambpdb tool from the AmberTools MD package.
    
    options:
      -h, --help            show this help message and exit
      --config CONFIG       Configuration file
    
    required arguments:
      --input_top_path INPUT_TOP_PATH
                            AMBER topology file. Accepted formats: top, parmtop, prmtop.
      --input_crd_path INPUT_CRD_PATH
                            AMBER coordinates file. Accepted formats: crd, mdcrd, inpcrd.
      --output_pdb_path OUTPUT_PDB_PATH
                            Structure PDB file. Accepted formats: pdb.
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_top_path** (*string*): AMBER topology file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/ambpdb/structure.leap.top). Accepted formats: TOP, PARMTOP, PRMTOP
* **input_crd_path** (*string*): AMBER coordinates file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/ambpdb/structure.leap.crd). Accepted formats: CRD, MDCRD, INPCRD, RST
* **output_pdb_path** (*string*): Structure PDB file. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/ambpdb/structure.ambpdb.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **binary_path** (*string*): (ambpdb) Path to the ambpdb executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
* **container_path** (*string*): (None) Container path definition..
* **container_image** (*string*): (afandiadib/ambertools:serial) Container image definition..
* **container_volume_path** (*string*): (/tmp) Container volume path definition..
* **container_working_dir** (*string*): (None) Container working directory definition..
* **container_user_id** (*string*): (None) Container user_id definition..
* **container_shell_path** (*string*): (/bin/bash) Path to default shell inside the container..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_amber_to_pdb.yml)
```python
properties:
  remove_tmp: true

```
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_amber_to_pdb_docker.yml)
```python
properties:
  container_image: afandiadib/ambertools:serial
  container_path: docker
  container_volume_path: /tmp

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
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_amber_to_pdb_docker.json)
```python
{
  "properties": {
    "container_path": "docker",
    "container_image": "afandiadib/ambertools:serial",
    "container_volume_path": "/tmp"
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
    usage: leap_gen_top [-h] [--config CONFIG] --input_pdb_path INPUT_PDB_PATH [--input_lib_path INPUT_LIB_PATH] [--input_frcmod_path INPUT_FRCMOD_PATH] [--input_params_path INPUT_PARAMS_PATH] [--input_prep_path INPUT_PREP_PATH] [--input_source_path INPUT_SOURCE_PATH] --output_pdb_path OUTPUT_PDB_PATH --output_top_path OUTPUT_TOP_PATH --output_crd_path OUTPUT_CRD_PATH
    
    Generating a MD topology from a molecule structure using tLeap program from AmberTools MD package.
    
    options:
      -h, --help            show this help message and exit
      --config CONFIG       Configuration file
    
    required arguments:
      --input_pdb_path INPUT_PDB_PATH
                            Input 3D structure PDB file. Accepted formats: pdb.
      --input_lib_path INPUT_LIB_PATH
                            Input ligand library parameters file. Accepted formats: lib, zip.
      --input_frcmod_path INPUT_FRCMOD_PATH
                            Input ligand frcmod parameters file. Accepted formats: frcmod, zip.
      --input_params_path INPUT_PARAMS_PATH
                            Additional leap parameter files to load with loadAmberParams Leap command. Accepted formats: leapin, in, txt, zip.
      --input_prep_path INPUT_PREP_PATH
                            Additional leap parameter files to load with loadAmberPrep Leap command. Accepted formats: leapin, in, txt, zip.
      --input_source_path INPUT_SOURCE_PATH
                            Additional leap command files to load with source Leap command. Accepted formats: leapin, in, txt, zip.
      --output_pdb_path OUTPUT_PDB_PATH
                            Output 3D structure PDB file matching the topology file. Accepted formats: pdb.
      --output_top_path OUTPUT_TOP_PATH
                            Output topology file (AMBER ParmTop). Accepted formats: top.
      --output_crd_path OUTPUT_CRD_PATH
                            Output coordinates file (AMBER crd). Accepted formats: crd.
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input 3D structure PDB file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/structure.leapin.pdb). Accepted formats: PDB
* **input_lib_path** (*string*): Input ligand library parameters file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/ligand.lib). Accepted formats: LIB, ZIP
* **input_frcmod_path** (*string*): Input ligand frcmod parameters file. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/ligand.frcmod). Accepted formats: FRCMOD, ZIP
* **input_params_path** (*string*): Additional leap parameter files to load with loadAmberParams Leap command. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/frcmod.ionsdang_spce.txt). Accepted formats: IN, LEAPIN, TXT, ZIP
* **input_prep_path** (*string*): Additional leap parameter files to load with loadAmberPrep Leap command. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/heme_all.in). Accepted formats: IN, LEAPIN, TXT, ZIP
* **input_source_path** (*string*): Additional leap command files to load with source Leap command. File type: input. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/leaprc.water.spce.txt). Accepted formats: IN, LEAPIN, TXT, ZIP
* **output_pdb_path** (*string*): Output 3D structure PDB file matching the topology file. File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.leap.pdb). Accepted formats: PDB
* **output_top_path** (*string*): Output topology file (AMBER ParmTop). File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.leap.top). Accepted formats: TOP, PARMTOP, PRMTOP
* **output_crd_path** (*string*): Output coordinates file (AMBER crd). File type: output. [Sample file](https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.leap.crd). Accepted formats: CRD, MDCRD, INPCRD
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **forcefield** (*array*): ([protein.ff14SB,DNA.bsc1,gaff]) Forcefields to be used for the structure generation. Each item should be either a path to a leaprc file or a string with the leaprc file name if the force field is included with Amber (e.g. "/path/to/leaprc.protein.ff14SB" or "protein.ff14SB"). Default values: ["protein.ff14SB","DNA.bsc1","gaff"]..
* **binary_path** (*string*): (tleap) Path to the tleap executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
* **container_path** (*string*): (None) Container path definition..
* **container_image** (*string*): (afandiadib/ambertools:serial) Container image definition..
* **container_volume_path** (*string*): (/tmp) Container volume path definition..
* **container_working_dir** (*string*): (None) Container working directory definition..
* **container_user_id** (*string*): (None) Container user_id definition..
* **container_shell_path** (*string*): (/bin/bash) Path to default shell inside the container..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_leap_gen_top.yml)
```python
properties:
  forcefield:
  - protein.ff14SB
  remove_tmp: true

```
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_leap_gen_top_docker.yml)
```python
properties:
  container_image: afandiadib/ambertools:serial
  container_path: docker
  container_volume_path: /tmp
  forcefield:
  - protein.ff14SB

```
#### Command line
```python
leap_gen_top --config config_leap_gen_top.yml --input_pdb_path structure.leapin.pdb --input_lib_path ligand.lib --input_frcmod_path ligand.frcmod --input_params_path frcmod.ionsdang_spce.txt --input_prep_path heme_all.in --input_source_path leaprc.water.spce.txt --output_pdb_path structure.leap.pdb --output_top_path structure.leap.top --output_crd_path structure.leap.crd
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
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_leap_gen_top_docker.json)
```python
{
  "properties": {
    "forcefield": [
      "protein.ff14SB"
    ],
    "container_path": "docker",
    "container_image": "afandiadib/ambertools:serial",
    "container_volume_path": "/tmp"
  }
}
```
#### Command line
```python
leap_gen_top --config config_leap_gen_top.json --input_pdb_path structure.leapin.pdb --input_lib_path ligand.lib --input_frcmod_path ligand.frcmod --input_params_path frcmod.ionsdang_spce.txt --input_prep_path heme_all.in --input_source_path leaprc.water.spce.txt --output_pdb_path structure.leap.pdb --output_top_path structure.leap.top --output_crd_path structure.leap.crd
```

## Parmed_cpinutil
Wrapper of the AmberTools (AMBER MD Package) parmed tool module.
### Get help
Command:
```python
parmed_cpinutil -h
```
    usage: parmed_cpinutil [-h] [--config CONFIG] --input_top_path INPUT_TOP_PATH --output_cpin_path OUTPUT_CPIN_PATH [--output_top_path OUTPUT_TOP_PATH]
    
    create a cpin file for constant pH simulations from an AMBER topology file using parmed program from AmberTools MD package.
    
    options:
      -h, --help            show this help message and exit
      --config CONFIG       Configuration file
    
    required arguments:
      --input_top_path INPUT_TOP_PATH
                            Input AMBER topology file. Accepted formats: top, parmtop, prmtop.
      --output_cpin_path OUTPUT_CPIN_PATH
                            Output AMBER constant pH input (CPin) file. Accepted formats: cpin.
      --output_top_path OUTPUT_TOP_PATH
                            Output topology file (AMBER ParmTop). Accepted formats: top, parmtop, prmtop.
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
* **binary_path** (*string*): (cpinutil.py) Path to the cpinutil.py executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
* **container_path** (*string*): (None) Container path definition..
* **container_image** (*string*): (afandiadib/ambertools:serial) Container image definition..
* **container_volume_path** (*string*): (/tmp) Container volume path definition..
* **container_working_dir** (*string*): (None) Container working directory definition..
* **container_user_id** (*string*): (None) Container user_id definition..
* **container_shell_path** (*string*): (/bin/bash) Path to default shell inside the container..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_parmed_cpinutil.yml)
```python
properties:
  igb: 2
  remove_tmp: true
  resnames: AS4 GL4
  system: cln025

```
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_parmed_cpinutil_docker.yml)
```python
properties:
  container_image: afandiadib/ambertools:serial
  container_path: docker
  container_volume_path: /tmp
  igb: 2
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
#### [Docker config file](https://github.com/bioexcel/biobb_amber/blob/master/biobb_amber/test/data/config/config_parmed_cpinutil_docker.json)
```python
{
  "properties": {
    "igb": 2,
    "resnames": "AS4 GL4",
    "system": "cln025",
    "container_path": "docker",
    "container_image": "afandiadib/ambertools:serial",
    "container_volume_path": "/tmp"
  }
}
```
#### Command line
```python
parmed_cpinutil --config config_parmed_cpinutil.json --input_top_path structure.solv.top --output_cpin_path cln025.cpin --output_top_path cln025.cpH.prmtop
```
