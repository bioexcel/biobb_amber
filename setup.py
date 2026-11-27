import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biobb_amber",
    version="5.4.0",
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
    install_requires=["biobb_common==5.4.0"],
    python_requires=">=3.11",
    entry_points={
        "console_scripts": [
            "amber_to_pdb = biobb_amber.ambpdb.amber_to_pdb:AmberToPDB.main",
            "cestats_run = biobb_amber.cphstats.cestats_run:CestatsRun.main",
            "cphstats_run = biobb_amber.cphstats.cphstats_run:CphstatsRun.main",
            "cpptraj_randomize_ions = biobb_amber.cpptraj.cpptraj_randomize_ions:CpptrajRandomizeIons.main",
            "leap_add_ions = biobb_amber.leap.leap_add_ions:LeapAddIons.main",
            "leap_build_linear_structure = biobb_amber.leap.leap_build_linear_structure:LeapBuildLinearStructure.main",
            "leap_gen_top = biobb_amber.leap.leap_gen_top:LeapGenTop.main",
            "leap_solvate = biobb_amber.leap.leap_solvate:LeapSolvate.main",
            "parmed_cpinutil = biobb_amber.parmed.parmed_cpinutil:ParmedCpinUtil.main",
            "parmed_hmassrepartition = biobb_amber.parmed.parmed_hmassrepartition:ParmedHMassRepartition.main",
            "pdb4amber_run = biobb_amber.pdb4amber.pdb4amber_run:Pdb4amberRun.main",
            "pmemd_mdrun = biobb_amber.pmemd.pmemd_mdrun:PmemdMDRun.main",
            "process_mdout = biobb_amber.process.process_mdout:ProcessMDOut.main",
            "process_minout = biobb_amber.process.process_minout:ProcessMinOut.main",
            "sander_mdrun = biobb_amber.sander.sander_mdrun:SanderMDRun.main",
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: Unix",
    ],
)
