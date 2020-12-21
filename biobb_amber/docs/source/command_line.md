
# BioBB Template Command Line Help

Generic usage:


```python
biobb_command [-h] --config CONFIG --input_file(s) <input_file(s)> --output_file <output_file>
```

For more information about how to configurate binaries in your conda environment, please go to [Execution in command line](https://biobb-documentation.readthedocs.io/en/latest/execution.html#execution-in-command-line) section in the official documentation.

***

## Template

Description for the template module.

### Get help

Command:


```python
template -h
```


```python
usage: template [-h] [--config CONFIG] --input_file_path1 INPUT_FILE_PATH1 [--input_file_path2 INPUT_FILE_PATH2] --output_file_path OUTPUT_FILE_PATH

Description for the template module.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Configuration file
  --input_file_path2 INPUT_FILE_PATH2
                        Description for the second input file path (optional). Accepted formats: dcd.

required arguments:
  --input_file_path1 INPUT_FILE_PATH1
                        Description for the first input file path. Accepted formats: top.
  --output_file_path OUTPUT_FILE_PATH
                        Description for the output file path. Accepted formats: zip.
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_file_path1** (str): Description for the first input file path. File type: input. ``` `Sample file <https://urlto.sample>`_ ```. Accepted formats: top.
* **input_file_path2** (str) (Optional): Description for the second input file path (optional). File type: input. ``` `Sample file <https://urlto.sample>`_ ```. Accepted formats: dcd.
* **output_file_path** (str): Description for the output file path. File type: output. ``` `Sample file <https://urlto.sample>`_ ```. Accepted formats: zip.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
    
* **boolean_property** (*bool*) - (True) Example of boolean property.
* **executable_binary_property** (*str*) - ("zip") Example of executable binary property.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

### YAML

#### Config file (template.yml)


```python
properties:
  boolean_property: false
  remove_tmp: true
```

#### Command line


```python
template --config data/conf/template.yml --input_file_path1 data/input/topology.top --input_file_path2 data/input/trajectory.dcd --output_file_path data/output/output.zip
```

### JSON

#### Config file (template.json)


```python
{
  "properties": {
    "boolean_property": false,
    "remove_tmp": true
  }
}
```

#### Command line


```python
template --config data/conf/template.json --input_file_path1 data/input/topology.top --input_file_path2 data/input/trajectory.dcd --output_file_path data/output/output.zip
```

## TemplateContainer

Description for the template_container module.

### Get help

Command:


```python
template_container -h
```


```python
usage: template_container [-h] [--config CONFIG] --input_file_path1 INPUT_FILE_PATH1 [--input_file_path2 INPUT_FILE_PATH2] --output_file_path OUTPUT_FILE_PATH

Description for the template module.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Configuration file
  --input_file_path2 INPUT_FILE_PATH2
                        Description for the second input file path (optional). Accepted formats: dcd.

required arguments:
  --input_file_path1 INPUT_FILE_PATH1
                        Description for the first input file path. Accepted formats: top.
  --output_file_path OUTPUT_FILE_PATH
                        Description for the output file path. Accepted formats: zip.
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_file_path1** (str): Description for the first input file path. File type: input. ``` `Sample file <https://urlto.sample>`_ ```. Accepted formats: top.
* **input_file_path2** (str) (Optional): Description for the second input file path (optional). File type: input. ``` `Sample file <https://urlto.sample>`_ ```. Accepted formats: dcd.
* **output_file_path** (str): Description for the output file path. File type: output. ``` `Sample file <https://urlto.sample>`_ ```. Accepted formats: zip.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
    
* **boolean_property** (*bool*) - (True) Example of boolean property.
* **executable_binary_property** (*str*) - ("zip") Example of executable binary property.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
* **container_path** (*string*) - (None) Container path definition.
* **container_image** (*string*) - ('image/image:latest') Container image definition.
* **container_volume_path** (*string*) - ('/tmp') Container volume path definition.
* **container_working_dir** (*string*) - (None) Container working directory definition.
* **container_user_id** (*string*) - (None) Container user_id definition.
* **container_shell_path** (*string*) - ('/bin/bash') Path to default shell inside the container.

### YAML

#### Docker config file (template_docker.yml)


```python
properties:
  boolean_property: false
  remove_tmp: true
  container_path: docker
  container_image: mmbirb/zip:latest
  container_volume_path: /tmp
```

#### Command line


```python
template_container --config data/conf/template_docker.yml --input_file_path1 data/input/topology.top --input_file_path2 data/input/trajectory.dcd --output_file_path data/output/output.docker.zip
```

#### Singularity config file (template_singularity.yml)


```python
properties:
  boolean_property: false
  remove_tmp: true
  executable_binary_property: /opt/conda/bin/zip
  container_path: singularity
  container_image: zip.sif
  container_volume_path: /tmp
```

#### Command line


```python
template_container --config data/conf/template_singularity.yml --input_file_path1 data/input/topology.top --input_file_path2 data/input/trajectory.dcd --output_file_path data/output/output.singularity.zip
```

### JSON

#### Docker config file (template_docker.json)


```python
{
  "properties": {
    "boolean_property": false,
    "remove_tmp": true,
    "container_path": "docker",
    "container_image": "mmbirb/zip:latest",
    "container_volume_path": "/tmp"
  }
}
```

#### Command line


```python
template_container --config data/conf/template_docker.json --input_file_path1 data/input/topology.top --input_file_path2 data/input/trajectory.dcd --output_file_path data/output/output.docker.zip
```

#### Singularity config file (template_singularity.json)


```python
{
  "properties": {
    "boolean_property": false,
    "remove_tmp": true,
    "executable_binary_property": "/opt/conda/bin/zip",
    "container_path": "singularity",
    "container_image": "zip.sif",
    "container_volume_path": "/tmp"
  }
}
```

#### Command line


```python
template_container --config data/conf/template_singularity.json --input_file_path1 data/input/topology.top --input_file_path2 data/input/trajectory.dcd --output_file_path data/output/output.singularity.zip
```
