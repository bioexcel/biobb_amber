[![](https://img.shields.io/github/v/tag/bioexcel/biobb_amber?label=Version)](https://GitHub.com/bioexcel/biobb_amber/tags/)
[![](https://img.shields.io/pypi/v/biobb-amber.svg?label=Pypi)](https://pypi.python.org/pypi/biobb-amber/)
[![](https://img.shields.io/conda/vn/bioconda/biobb_amber?label=Conda)](https://anaconda.org/bioconda/biobb_amber)
[![](https://img.shields.io/conda/dn/bioconda/biobb_amber?label=Conda%20Downloads)](https://anaconda.org/bioconda/biobb_amber)
[![](https://img.shields.io/badge/Docker-Quay.io-blue)](https://quay.io/repository/biocontainers/biobb_amber?tab=tags)
[![](https://img.shields.io/badge/Singularity-GalaxyProject-blue)](https://depot.galaxyproject.org/singularity/biobb_amber:5.0.4--pyhdfd78af_0)

[![](https://img.shields.io/badge/OS-Unix%20%7C%20MacOS-blue)](https://github.com/bioexcel/biobb_amber)
[![](https://img.shields.io/pypi/pyversions/biobb-amber.svg?label=Python%20Versions)](https://pypi.org/project/biobb-amber/)
[![](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![](https://img.shields.io/badge/Open%20Source%3f-Yes!-blue)](https://github.com/bioexcel/biobb_amber)

[![](https://readthedocs.org/projects/biobb-amber/badge/?version=latest&label=Docs)](https://biobb-amber.readthedocs.io/en/latest/?badge=latest)
[![](https://img.shields.io/website?down_message=Offline&label=Biobb%20Website&up_message=Online&url=https%3A%2F%2Fmmb.irbbarcelona.org%2Fbiobb%2F)](https://mmb.irbbarcelona.org/biobb/)
[![](https://img.shields.io/badge/Youtube-tutorials-blue?logo=youtube&logoColor=red)](https://www.youtube.com/@BioExcelCoE/search?query=biobb)
[![](https://zenodo.org/badge/DOI/10.1038/s41597-019-0177-4.svg)](https://doi.org/10.1038/s41597-019-0177-4)
[![](https://img.shields.io/endpoint?color=brightgreen&url=https%3A%2F%2Fapi.juleskreuer.eu%2Fcitation-badge.php%3Fshield%26doi%3D10.1038%2Fs41597-019-0177-4)](https://www.nature.com/articles/s41597-019-0177-4#citeas)

[![](https://docs.bioexcel.eu/biobb_amber/junit/testsbadge.svg)](https://docs.bioexcel.eu/biobb_amber/junit/report.html)
[![](https://docs.bioexcel.eu/biobb_amber/coverage/coveragebadge.svg)](https://docs.bioexcel.eu/biobb_amber/coverage/)
[![](https://docs.bioexcel.eu/biobb_amber/flake8/flake8badge.svg)](https://docs.bioexcel.eu/biobb_amber/flake8/)
[![](https://img.shields.io/github/last-commit/bioexcel/biobb_amber?label=Last%20Commit)](https://github.com/bioexcel/biobb_amber/commits/master)
[![](https://img.shields.io/github/issues/bioexcel/biobb_amber.svg?color=brightgreen&label=Issues)](https://GitHub.com/bioexcel/biobb_amber/issues/)

[![fair-software.eu](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F-green)](https://fair-software.eu)
[![](https://www.bestpractices.dev/projects/8847/badge)](https://www.bestpractices.dev/projects/8847)

[](https://bestpractices.coreinfrastructure.org/projects/8847/badge)

[//]: # (The previous line invisible link is for compatibility with the howfairis script https://github.com/fair-software/howfairis-github-action/tree/main wich uses the old bestpractices URL)

# biobb_amber

### Introduction
biobb_amber is a BioBB category for AMBER MD package.
biobb_amber allows setup and simulation of atomistic MD simulations using AMBER MD package and its associated AMBER tools.
Biobb (BioExcel building blocks) packages are Python building blocks that
create new layer of compatibility and interoperability over popular
bioinformatics tools.
The latest documentation of this package can be found in our readthedocs site:
[latest API documentation](http://biobb-amber.readthedocs.io/en/latest/).

### Version
v5.0.4 2024.2

### Installation
Using PIP:

> **Important:** PIP only installs the package. All the dependencies must be installed separately. To perform a complete installation, please use ANACONDA or DOCKER.

* Installation:


        pip install "biobb_amber>=5.0.4"


* Usage: [Python API documentation](https://biobb-amber.readthedocs.io/en/latest/modules.html)

Using ANACONDA:

* Installation:


        conda install -c bioconda "biobb_amber>=5.0.4"


* Usage: With conda installation BioBBs can be used with the [Python API documentation](https://biobb-amber.readthedocs.io/en/latest/modules.html) and the [Command Line documentation](https://biobb-amber.readthedocs.io/en/latest/command_line.html)

Using DOCKER:

* Installation:


        docker pull quay.io/biocontainers/biobb_amber:5.0.4--pyhdfd78af_0


* Usage:


        docker run quay.io/biocontainers/biobb_amber:5.0.4--pyhdfd78af_0


Using SINGULARITY:

**MacOS users**: it's strongly recommended to avoid Singularity and use **Docker** as containerization system.

* Installation:


        singularity pull --name biobb_amber.sif https://depot.galaxyproject.org/singularity/biobb_amber:5.0.4--pyhdfd78af_0


* Usage:


        singularity exec biobb_amber.sif <command>


The command list and specification can be found at the [Command Line documentation](https://biobb-amber.readthedocs.io/en/latest/command_line.html).

### Copyright & Licensing
This software has been developed in the [MMB group](http://mmb.irbbarcelona.org) at the [BSC](http://www.bsc.es/) & [IRB](https://www.irbbarcelona.org/) for the [European BioExcel](http://bioexcel.eu/), funded by the European Commission (EU H2020 [823830](http://cordis.europa.eu/projects/823830), EU H2020 [675728](http://cordis.europa.eu/projects/675728)).

* (c) 2015-2025 [Barcelona Supercomputing Center](https://www.bsc.es/)
* (c) 2015-2025 [Institute for Research in Biomedicine](https://www.irbbarcelona.org/)

Licensed under the
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0), see the file LICENSE for details.

![](https://bioexcel.eu/wp-content/uploads/2019/04/Bioexcell_logo_1080px_transp.png "Bioexcel")
