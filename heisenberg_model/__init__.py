# -*- coding: utf-8 -*-

# This code is part of heisenberg_model.
#
# (C) Copyright NTNU QuCAI-Lab, 2022.
#
# This code is licensed under the Apache 2.0 License. 
# You may obtain a copy of the License in the root directory of this source tree.

"""NTNU QuCAI-Lab heisenberg-model 2022"""

import os

VERSION_PATH = os.path.join(os.path.dirname(__file__), "VERSION.txt")
with open(VERSION_PATH, "r") as version_file:
  VERSION = version_file.read().strip()
    
__name__ = "heisenberg_model"
__version__ = VERSION
__status__ = "Development"
__homepage__ = "https://github.com/QuCAI-Lab/ibm2021-open-science-prize"
__author__ = "Lucas Camponogara Viera"
__license__ = "Apache 2.0"
__copyright__ = "Copyright QuCAI-Lab 2022"

###########################################################################

# Sanity Check 
from . import sanity 

# Requirements 
import sys
import qiskit 
import numpy as np

# About
def about():
  """Function to display the heisenberg-model project information."""
  print(" \
    ###################################\n \
    Heisenberg Model PROJECT INFORMATION:\n \
    >> Simulating the XXX Heisenberg Model Hamiltonian for a System of Three Interacting Spin-1/2 Particles on IBM Quantum’s 7-qubit Jakarta Processor.\n \
    ###################################\n"
     )
  print(f"{__copyright__}")
  print(f"Name: {__name__}")
  print(f"Version: {__version__}")
  print(f"Status: {__status__}")
  print(f"Home-page: {__homepage__}")
  print(f"Author: {__author__}")
  print(f"License: {__license__}")
  print(f"Requires: python=={sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}, qiskit=={qiskit.__version__}, numpy=={np.__version__}")
  
# Simulation
from .main.classical_simulation import ClassicalSimulation
from .main.quantum_simulation import QuantumSimulation
