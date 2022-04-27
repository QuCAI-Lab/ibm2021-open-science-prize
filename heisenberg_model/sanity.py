# -*- coding: utf-8 -*-

# This code is part of heisenberg_model.
#
# (C) Copyright NTNU QuCAI-Lab, 2022.
#
# This code is licensed under the Apache 2.0 License. 
# You may obtain a copy of the License in the root directory of this source tree.

"""Check for installed dependencies"""

###########################################################################
import os

try:
  import numpy
except ImportError:
  print(" \
      ###################################\n \
      WARNING:\n \
      >> This package depends on NumPy.\n \
      >> To install NumPy, run: $ python3 -m pip install numpy==1.20.1\n \
      ###################################\n"
       )
try:
  import qiskit
except ImportError:
  print(" \
      ###################################\n \
      WARNING:\n \
      >> This package depends on Qiskit SDK\n \
      >> To install Qiskit, run: $ python3 -m pip install qiskit==0.35.0\n \
      ###################################\n"
       )
  raise
