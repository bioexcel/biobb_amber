import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biobb_amber",
    version="5.0.4",
    author="Biobb developers",
    author_email="adam.hospital@irbbarcelona.org",
    description="Biobb_amber is a BioBB category for AMBER MD package.",
    long_description="Biobb_amber allows setup and simulation of atomistic MD simulations using AMBER MD package and its associated AMBER tools.",
    long_description_content_type="text/markdown",
    keywords="Bioinformatics Workflows BioExcel Compatibility MD Amber",
    url="https://github.com/bioexcel/biobb_amber",
    project_urls={
        "Documentation": "http://biobb-amber.readthedocs.io/en/latest/",
        "Bioexcel": "https://bioexcel.eu/",
    },
    packages=setuptools.find_packages(exclude=["docs", "test"]),
    package_data={"biobb_amber": ["py.typed"]},
    install_requires=["biobb_common==5.0.0"],
    python_requires=">=3.9, <3.11",
    entry_points={
        "console_scripts": [
            "amber_to_pdb = biobb_amber.ambpdb.amber_to_pdb:main",
            "cestats_run = biobb_amber.cphstats.cestats_run:main",
            "cphstats_run = biobb_amber.cphstats.cphstats_run:main",
            "cpptraj_randomize_ions = biobb_amber.cpptraj.cpptraj_randomize_ions:main",
            "leap_add_ions = biobb_amber.leap.leap_add_ions:main",
            "leap_build_linear_structure = biobb_amber.leap.leap_build_linear_structure:main",
            "leap_gen_top = biobb_amber.leap.leap_gen_top:main",
            "leap_solvate = biobb_amber.leap.leap_solvate:main",
            "nab_build_dna_structure = biobb_amber.nab.nab_build_dna_structure:main",
            "parmed_cpinutil = biobb_amber.parmed.parmed_cpinutil:main",
            "parmed_hmassrepartition = biobb_amber.parmed.parmed_hmassrepartition:main",
            "pdb4amber_run = biobb_amber.pdb4amber.pdb4amber_run:main",
            "pmemd_mdrun = biobb_amber.pmemd.pmemd_mdrun:main",
            "process_mdout = biobb_amber.process.process_mdout:main",
            "process_minout = biobb_amber.process.process_minout:main",
            "sander_mdrun = biobb_amber.sander.sander_mdrun:main",
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: Unix",
    ],
)
