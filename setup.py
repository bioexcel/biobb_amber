import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biobb_amber",
    version="3.5.0",
    author="Biobb developers",
    author_email="adam.hospital@irbbarcelona.org",
    description="Biobb_amber is a BioBB category for AMBER MD package.",
    long_description="Biobb_amber allows setup and simulation of atomistic MD simulations using AMBER MD package and its associated AMBER tools.",
    long_description_content_type="text/markdown",
    keywords="Bioinformatics Workflows BioExcel Compatibility MD Amber",
    url="https://github.com/bioexcel/biobb_amber",
    project_urls={
        "Documentation": "http://biobb_amber.readthedocs.io/en/latest/",
        "Bioexcel": "https://bioexcel.eu/"
    },
    packages=setuptools.find_packages(exclude=['docs', 'test']),
    install_requires=['biobb_common>=3.5.1'],
    python_requires='==3.7.*',
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
    ),
)