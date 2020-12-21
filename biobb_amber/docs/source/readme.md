[![](https://readthedocs.org/projects/biobb-amber/badge/?version=latest)](https://biobb-amber.readthedocs.io/en/latest/?badge=latest)


# biobb_amber

### Introduction
biobb_amber is a BioBB category for AMBER MD package.
biobb_amber allows setup and simulation of atomistic MD simulations using AMBER MD package and its associated AMBER tools.
Biobb (BioExcel building blocks) packages are Python building blocks that
create new layer of compatibility and interoperability over popular
bioinformatics tools.
The latest documentation of this package can be found in our readthedocs site:
[latest API documentation](http://biobb_amber.readthedocs.io/en/latest/).

### Version
v3.5.0 2020.4

### Installation
Using PIP:

> **Important:** PIP only installs the package. All the dependencies must be installed separately. To perform a complete installation, please use ANACONDA, DOCKER or SINGULARITY.

* Installation:


        pip install "biobb_amber>=3.5.0"


* Usage: [Python API documentation](https://biobb-amber.readthedocs.io/en/latest/modules.html)

Using ANACONDA:

* Installation:


        conda install -c bioconda "biobb_amber>=3.5.0"


* Usage: With conda installation BioBBs can be used with the [Python API documentation](https://biobb-amber.readthedocs.io/en/latest/modules.html) and the [Command Line documentation](https://biobb-amber.readthedocs.io/en/latest/command_line.html)

Using DOCKER:

* Installation:


        docker pull quay.io/biocontainers/biobb_amber:3.5.0--py_0


* Usage:


        docker run quay.io/biocontainers/biobb_amber:3.5.0--py_0 <command>


Using SINGULARITY:

**MacOS users**: it's strongly recommended to avoid Singularity and use **Docker** as containerization system.
If you have no experience with anaconda, please first take a look to the [New with anaconda?](https://biobb-documentation.readthedocs.io/en/latest/first_steps.html#new-with-anaconda) section of the [official documentation](https://biobb-documentation.readthedocs.io/en/latest/).

* Installation:
Clone repository to your computer and create new conda environment:

```console
git https://github.com/bioexcel/biobb_amber.git
cd biobb_amber
conda env create -f conda_env/environment.yml
```

        singularity pull --name biobb_amber.sif shub://bioexcel/biobb_amber
Edit **conda_env/biobb_amber.pth** with the paths to your *biobb_amber* folder. Example:

```console
/home/user_name/projects/biobb_amber/
/home/user_name/projects/biobb_amber/biobb_amber/biobb_amber
```

* Usage:
Copy the edited **conda_env/biobb_amber.pth** file to the site-packages folder of your environment. This folder is in */[anaconda-path]/envs/biobb_amber/lib/python3.6/site-packages*, where */[anaconda-path]* is usually */anaconda3* or */opt/conda*. Then, activate the recently created *biobb_amber* conda environment.

```console
cp conda_env/biobb_amber.pth /[anaconda-path]/envs/biobb_amber/lib/python3.6/site-packages
conda activate biobb_amber
```

        singularity exec biobb_amber.sif <command>
Additionnally, it's recommendable to configure binary paths in your environment in order to easy the command line execution. More info about this subject in the [Binary path configuration](https://biobb-documentation.readthedocs.io/en/latest/execution.html#binary-path-configuration) section of the [official documentation](https://biobb-documentation.readthedocs.io/en/latest/).

### Documentation

The command list and specification can be found at the [Command Line documentation](https://biobb-amber.readthedocs.io/en/latest/command_line.html).
[Click here to find the API Documentation example](https://biobb-template.readthedocs.io/en/latest/template.html) for this template and [here for Command Line documentation](http://biobb_amber.readthedocs.io/en/latest/command_line.html).

And here you can find [the full documentation](https://biobb-documentation.readthedocs.io/en/latest/) about how to build a new **BioExcel building block** from scratch.

### Copyright & Licensing
This software has been developed in the [MMB group](http://mmb.irbbarcelona.org) at the [BSC](http://www.bsc.es/) & [IRB](https://www.irbbarcelona.org/) for the [European BioExcel](http://bioexcel.eu/), funded by the European Commission (EU H2020 [823830](http://cordis.europa.eu/projects/823830), EU H2020 [675728](http://cordis.europa.eu/projects/675728)).
