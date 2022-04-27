#!/usr/bin/python3
# Shebang line to identify this file as a python script.

# -*- coding: utf-8 -*-
# PEP 0263 encoding. Line declared in case you decide to use an encoding other than python3 default UTF-8 or support python2.x.

# This code is part of heisenberg_model.
#
# (C) Copyright NTNU QuCAI-Lab, 2022.
#
# This code is licensed under the Apache 2.0 License. 
# You may obtain a copy of the License in the root directory of this source tree.

'''Main module to run the Classical simulation of the XXX Heisenberg Model Hamiltonian for a three particle system.'''

import matplotlib.pyplot as plt
from qiskit.quantum_info import state_fidelity
from qiskit.opflow import Zero, One, I, X, Y, Z
from scipy.linalg import expm
import numpy as np

class ClassicalSimulation():
  def __init__(self, trotter_steps, time, measured_state, prepared_state):
    self.trotter_steps = trotter_steps
    self.time=time
    self.measured_state=measured_state
    self.prepared_state=prepared_state
    self.sigma0 = np.array([[1,0],[0,1]])
    self.sigma1 = np.array([[0,1],[1,0]])
    self.sigma2 = np.array([[0,-1j],[1j,0]])
    self.sigma3 = np.array([[1,0],[0,-1]])
  
  def plot(self, xlabel, ylabel, title, legends=True, size=False, **kwargs):
    '''
    Function for plot visualization.
    
    Args:
      - xlabel (str): the X-axis label.
      - ylabel (str): the Y-axis label.
      - title (str): the title of the plot.
      - legends (bool): boolean value to determine if labels are applied. Default is True.
      - size (bool): boolean value to determine if image size, resolution and plot are applied. Default is False.
    
    **kwargs
      - x (numpy.ndarray): set of X-axis values.
      - y (list): set of Y-axis values.
      - w (int): width of the plot figure in unit inches.
      - h (int): height of the plot figure in unit inches.
      - dpi (int): resolution in dots per inch.
    '''
    if kwargs:
        x, y, w, h, dpi = kwargs.values()
    if size:
        plt.figure(figsize = (w,h), dpi = dpi)
        plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if legends:
        plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    plt.title(title)
    plt.grid()
    plt.show()

  def ham_decomposition_num(self):
    '''
    Method that decomposes the XXX Heisenberg Hamiltonian using NumPy.
    
    Returns:
      - h_a, h_b (tuple): the reduced Hamiltonians of the decomposition, each of type=numpy.ndarray.
    '''
    ham_num = np.kron(self.sigma1, self.sigma1) + np.kron(self.sigma2, self.sigma2) + np.kron(self.sigma3, self.sigma3)
    h_a = np.kron(ham_num, self.sigma0)
    h_b = np.kron(self.sigma0, ham_num)
    return h_a, h_b
  
  def trotter_evolution_num(self, time, hamiltonian, trotter_steps):
    '''
    Method that computes the Trotterization of the Evolution Operator given the XXX Heisenberg Hamiltonian using NumPy.
    
    Returns:
      - power (numpy.ndarray): the matrix representing the Evolution operator to the power of trotter_steps.
    '''
    h_a, h_b = hamiltonian
    evolution_operator_a=expm(-1j*float(time/trotter_steps)*h_a)
    evolution_operator_b=expm(-1j*float(time/trotter_steps)*h_b)
    evolution_operator=np.dot(evolution_operator_a, evolution_operator_b)
    power=np.linalg.matrix_power(evolution_operator, trotter_steps)
    return power 
 
  def state_fidelity_num(self, measured_state, prepared_state, time_window, unitary_evolution, hamiltonian, trotter_steps):
    '''    
    Function that computes the probability of measuring a given reference state of a quantum system evolving over time.
    
    If the reference_state is equal to the prepared_state, this function computes the modulus squared of the expectation value of a given operator over a given time window.

    Args:
      - measured_state (numpy.ndarray): a column (ket) vector representing the quantum state to be measured.
      - prepared_state (numpy.ndarray): a column (ket) vector representing the state in which the quantum system was prepared.
      - time_window (numpy.ndarray): array of time instants of the state evolution.
      - unitary_evolution (function): a function that returns the matrix representation (numpy.ndarray) of the Trottered Evolution operator.
      - hamiltonian (tuple): the reduced Hamiltonians from the decomposition, each of type=numpy.ndarray.
      - trotter_steps (int): the number of Trotter steps.

    Returns:
      - probability_array (numpy.ndarray): array with the individual probabilities of finding the quantum system in a given reference state at a given time instant.
    '''
    probability_array=np.zeros(len(time_window))
    adjoint = measured_state.conj().T
    for i in range(len(time_window)):
      unitary=unitary_evolution(time_window[i],hamiltonian,trotter_steps)
      evolved_state=np.dot(unitary, prepared_state)
      inner_product = np.dot(adjoint,evolved_state)
      probability_array[i] = np.abs(inner_product)**2   
        
    return probability_array
  
  def run_classical(self):
    '''
    Main method to run the classical simulation.
    '''
    time_window=np.arange(start=0, stop=self.time+0.01, step=0.01)
    fidelity=[]
    plt.figure(figsize = (6,4), dpi = 85)
    for i in range(self.trotter_steps):
      fids=self.state_fidelity_num(self.measured_state, self.prepared_state, time_window, self.trotter_evolution_num, self.ham_decomposition_num(), trotter_steps=i+1)
      fidelity.append(fids[len(time_window)-1])
      plt.plot(time_window, fids, label = f"F{i+1}")
    self.plot('Time', f'Probability of state $|110\\rangle$',f'Fidelity of state $|110\\rangle$ under $U_{{Trotter}}(t={int(self.time/np.pi)}\pi)$.',True,False)
    for value in fidelity:
      print(f'F{fidelity.index(value)+1}={value}') 
      
if __name__ == "__main__":
  import math
  init_state=(One^One^Zero).to_matrix()
  evolved=init_state
  csim=ClassicalSimulation(trotter_steps=9, time=math.pi, measured_state=evolved, prepared_state=init_state)
  csim.run_classical()
