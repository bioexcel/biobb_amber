# biobb_ml

### Introduction
Biobb_ml is the Biobb module collection to perform machine learning predictions.
Biobb (BioExcel building blocks) packages are Python building blocks that
create new layer of compatibility and interoperability over popular
bioinformatics tools.
The latest documentation of this package can be found in our readthedocs site:
[latest API documentation](http://biobb_ml.readthedocs.io/en/latest/).

### Version
v3.5.0 2020.4

### Installation
Using PIP:

> **Important:** PIP only installs the package. All the dependencies must be installed separately. To perform a complete installation, please use ANACONDA, DOCKER or SINGULARITY.

* Installation:


        pip install "biobb_ml>=3.5.0"


* Usage: [Python API documentation](https://biobb-ml.readthedocs.io/en/latest/modules.html)

Using ANACONDA:

* Installation:


        conda install -c bioconda "biobb_ml>=3.5.0"


* Usage: With conda installation BioBBs can be used with the [Python API documentation](https://biobb-ml.readthedocs.io/en/latest/modules.html) and the [Command Line documentation](https://biobb-ml.readthedocs.io/en/latest/command_line.html)

Using DOCKER:

* Installation:


        docker pull quay.io/biocontainers/biobb_ml:3.5.0--py_0


* Usage:


        docker run quay.io/biocontainers/biobb_ml:3.5.0--py_0 <command>


Using SINGULARITY:

**MacOS users**: it's strongly recommended to avoid Singularity and use **Docker** as containerization system.

* Installation:


        singularity pull --name biobb_ml.sif shub://bioexcel/biobb_ml


* Usage:


        singularity exec biobb_ml.sif <command>


The command list and specification can be found at the [Command Line documentation](https://biobb-ml.readthedocs.io/en/latest/command_line.html).

### Copyright & Licensing
This software has been developed in the [MMB group](http://mmb.irbbarcelona.org) at the [BSC](http://www.bsc.es/) & [IRB](https://www.irbbarcelona.org/) for the [European BioExcel](http://bioexcel.eu/), funded by the European Commission (EU H2020 [823830](http://cordis.europa.eu/projects/823830), EU H2020 [675728](http://cordis.europa.eu/projects/675728)).

* (c) 2015-2020 [Barcelona Supercomputing Center](https://www.bsc.es/)
* (c) 2015-2020 [Institute for Research in Biomedicine](https://www.irbbarcelona.org/)

Licensed under the
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0), see the file LICENSE for details.

![](https://bioexcel.eu/wp-content/uploads/2019/04/Bioexcell_logo_1080px_transp.png "Bioexcel")
