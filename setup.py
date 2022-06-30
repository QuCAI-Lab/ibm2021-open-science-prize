# This code is part of heisenberg-model.
#
# (C) Copyright NTNU QuCAI-Lab, 2022.
#
# This code is licensed under the Apache 2.0 License. 
# You may obtain a copy of the License in the root directory of this source tree.

"""A setuptools based setup configuration module (not Distutils) to specify the package information (metadata, contents, dependencies, etc.).

Since PEP 517, the setup.py file can now be replaced with the setup.cfg configuration file! 

Run this setup.py file using:
    $ python3 -m pip install -v -e .
    The "python3 -m pip install ." command is equivalent to the "python3 -m setup.py install" command.
    The -m flag in "python3 -m pip" enforce the pip version tied to the active environment (executes pip as the __main__ module).
    
Flags:
    -e, --editable <path/url>
        Install the package without copying any files to the interpreter directory allowing for source code changes to take effect without the use of rebuild and reinstall. 
        It also creates a <package_name>.egg-info file that enables the user to access the package information.
        For more information, see https://setuptools.pypa.io/en/latest/userguide/development_mode.html.
    -v, --verbose
        Enables progress display.

To create a source distribution file (which you can upload to PyPI) in the dist directory, simply run:
    $ python -m build

REFERENCES
[1] Setuptools, at "https://setuptools.pypa.io/en/latest/userguide/quickstart.html".
"""

import setuptools, inspect, os, sys
from pathlib import Path
from setuptools import setup, find_packages

if not hasattr(setuptools, 'find_namespace_packages') or not inspect.ismethod(setuptools.find_namespace_packages):
    print("Your setuptools version:'{}' does not support PEP 420 (find_namespace_packages). "
          "Upgrade it to version >='40.1.0' and repeat install.".format(setuptools.__version__))
    sys.exit(1)
    
here = Path(__file__).parent.absolute()  

with open(here / "README.md", encoding="utf-8") as f:
    long_description = f.read()
    
with open(here / "requirements.txt", encoding="utf-8") as f:
    requirements = f.read().splitlines()

VERSION_PATH = os.path.join(os.path.dirname(__file__), "heisenberg_model", "VERSION.txt")
with open(VERSION_PATH, "r") as version_file:
    VERSION = version_file.read().strip()
    
setup(
    name="heisenberg_model", # The name for your package, the same name given to the main folder of your File Structure (package tree).
    packages=find_packages(), # A list of packages to be manipulated. 
                              # If there is only one pure python module, set the variable to a list containing a single string value: packages = ["heisenberg_model"].
                              # This will make Setuptools to look for the heisenberg_model/__init__.py file that is required so that Python treat the directory as a package. 
                              # One can verify the above is true at https://setuptools.pypa.io/en/latest/userguide/quickstart.html and at https://docs.python.org/3/tutorial/modules.html.
    version=VERSION, # Defines the version format for your package.
    description="heisenberg-model | Simulating the XXX Heisenberg Model Hamiltonian for a System of Three Interacting Spin-1/2 Particles on IBM Quantum’s 7-qubit Jakarta Processor",
    long_description=long_description, # Defines the README.md file content as the description of the package.
    long_description_content_type="text/markdown",
    author="Lucas Camponogara Viera",
    author_email="vieracamponogara@gmail.com",
    download_url="https://github.com/QuCAI-Lab/ibm2021-open-science-prize", # A string specifying the URL to download the package.
    license="Apache 2.0", # One can choose a License template from: https://help.github.com/articles/licensing-a-repository.
    platforms=["Windows", "Linux"], # Defines a list of OS that runs the cross-platform application.
    classifiers=[
        "Development Status :: Alpha", # One can choose between "Alpha", "Beta" or "Production/Stable".
        "Environment :: Console",
        "License :: OSI Approved :: Creative Commons Software License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
    ], # Specifies the categories for the package in a list of strings.
    keywords=['heisenberg', 'hamiltonian', 'trotterization', 'qiskit', 'qubit', 'ibm', 'jakarta'], # Besides a list of strings, Keywords can also be specified in a comma-separated string format: keywords="Heisenberg Model".
    python_requires="==3.7.13", # A version specifier used to specify the Requires-Python defined in PEP 345.
    install_requires=requirements, # Specifies the 'requirements.txt' file that contains a list of required package dependencies to be installed.
    project_urls={
        "Bug Tracker": "https://github.com/QuCAI-Lab/ibm2021-open-science-prize/issues",
        "Documentation": "https://github.com/QuCAI-Lab/ibm2021-open-science-prize",
        "Source Code": "https://github.com/QuCAI-Lab/ibm2021-open-science-prize",
    },
)
