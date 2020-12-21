[![](https://readthedocs.org/projects/biobb-template/badge/?version=latest)](https://biobb-template.readthedocs.io/en/latest/?badge=latest)

# biobb_template

### Introduction
Biobb_template is a complete code template to promote and facilitate the creation of
new Biobbs by the community.
Biobb (BioExcel building blocks) packages are Python building blocks that
create new layer of compatibility and interoperability over popular
bioinformatics tools.
The latest documentation of this package can be found in our readthedocs site:
[latest API documentation](http://biobb_template.readthedocs.io/en/latest/).

### Version
v1.0.0 2020.1

### Installation

If you have no experience with anaconda, please first take a look to the [New with anaconda?](https://biobb-documentation.readthedocs.io/en/latest/first_steps.html#new-with-anaconda) section of the [official documentation](https://biobb-documentation.readthedocs.io/en/latest/).

Clone repository to your computer and create new conda environment:

```console
git https://github.com/bioexcel/biobb_template.git
cd biobb_template
conda env create -f conda_env/environment.yml
```

Edit **conda_env/biobb_template.pth** with the paths to your *biobb_template* folder. Example:

```console
/home/user_name/projects/biobb_template/
/home/user_name/projects/biobb_template/biobb_template/biobb_template
```

Copy the edited **conda_env/biobb_template.pth** file to the site-packages folder of your environment. This folder is in */[anaconda-path]/envs/biobb_template/lib/python3.6/site-packages*, where */[anaconda-path]* is usually */anaconda3* or */opt/conda*. Then, activate the recently created *biobb_template* conda environment.

```console
cp conda_env/biobb_template.pth /[anaconda-path]/envs/biobb_template/lib/python3.6/site-packages
conda activate biobb_template
```

Additionnally, it's recommendable to configure binary paths in your environment in order to easy the command line execution. More info about this subject in the [Binary path configuration](https://biobb-documentation.readthedocs.io/en/latest/execution.html#binary-path-configuration) section of the [official documentation](https://biobb-documentation.readthedocs.io/en/latest/).

### Documentation

[Click here to find the API Documentation example](https://biobb-template.readthedocs.io/en/latest/template.html) for this template and [here for Command Line documentation](http://biobb_template.readthedocs.io/en/latest/command_line.html).

And here you can find [the full documentation](https://biobb-documentation.readthedocs.io/en/latest/) about how to build a new **BioExcel building block** from scratch.

### Copyright & Licensing
This software has been developed in the [MMB group](http://mmb.irbbarcelona.org) at the [BSC](http://www.bsc.es/) & [IRB](https://www.irbbarcelona.org/) for the [European BioExcel](http://bioexcel.eu/), funded by the European Commission (EU H2020 [823830](http://cordis.europa.eu/projects/823830), EU H2020 [675728](http://cordis.europa.eu/projects/675728)).

* (c) 2015-2020 [Barcelona Supercomputing Center](https://www.bsc.es/)
* (c) 2015-2020 [Institute for Research in Biomedicine](https://www.irbbarcelona.org/)

Licensed under the
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0), see the file LICENSE for details.

![](https://bioexcel.eu/wp-content/uploads/2019/04/Bioexcell_logo_1080px_transp.png "Bioexcel")
