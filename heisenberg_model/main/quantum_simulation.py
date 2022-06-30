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

'''Main module to run the Quantum simulation of the XXX Heisenberg Model Hamiltonian for a three particle system.'''

# Importing standard Qiskit modules
from qiskit import QuantumCircuit, QuantumRegister, IBMQ, execute, transpile
from qiskit.providers.aer import QasmSimulator
from qiskit.tools.monitor import job_monitor
from qiskit.circuit import Parameter
from qiskit.opflow import Zero, One

# Importing state tomography modules
from qiskit.ignis.verification.tomography import state_tomography_circuits, StateTomographyFitter
from qiskit.quantum_info import state_fidelity

# Importing external module
from ibm_token import TOKEN # TOKEN is your IBM API token defined in a variable string type.
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Loading IBMQ account data
IBMQ.save_account(TOKEN, overwrite=True) 
provider = IBMQ.load_account()

# Connecting to IBM provider
provider = IBMQ.get_provider(hub='ibm-q-community', group='ibmquantumawards', project='open-science-22')
jakarta = provider.get_backend('ibmq_jakarta')

# Defining Jakarta-based quantum simulators
## Simulated backend based on ibmq_jakarta's device noise profile
sim_noisy_jakarta = QasmSimulator.from_backend(provider.get_backend('ibmq_jakarta'))
## Noiseless simulated backend
sim_noise_free = QasmSimulator()


class QuantumSimulation():
  def __init__(self, trotter_steps, target_time, reps, nshots):
    self.trotter_steps = trotter_steps
    self.time=target_time
    self.reps=reps
    self.shots=nshots
    self.message = 'Job in the queue...'
  
  def quantum_circuit(self):
    self.t = Parameter('t')
    
    # Build a subcircuit for XX(t) two-qubit gate
    XX_qr = QuantumRegister(2)
    XX_qc = QuantumCircuit(XX_qr, name='XX')
    XX_qc.ry(np.pi/2,[0,1])
    XX_qc.cnot(0,1)
    XX_qc.rz(2 * self.t, 1)
    XX_qc.cnot(0,1)
    XX_qc.ry(-np.pi/2,[0,1])
    # Convert custom quantum circuit into a gate
    XX = XX_qc.to_instruction()
  
    # Build a subcircuit for YY(t) two-qubit gate
    YY_qr = QuantumRegister(2)
    YY_qc = QuantumCircuit(YY_qr, name='YY')
    YY_qc.rx(np.pi/2,[0,1])
    YY_qc.cnot(0,1)
    YY_qc.rz(2 * self.t, 1)
    YY_qc.cnot(0,1)
    YY_qc.rx(-np.pi/2,[0,1])
    # Convert custom quantum circuit into a gate
    YY = YY_qc.to_instruction()

    # Build a subcircuit for ZZ(t) two-qubit gate
    ZZ_qr = QuantumRegister(2)
    ZZ_qc = QuantumCircuit(ZZ_qr, name='ZZ')
    ZZ_qc.cnot(0,1)
    ZZ_qc.rz(2 * self.t, 1)
    ZZ_qc.cnot(0,1)
    # Convert custom quantum circuit into a gate
    ZZ = ZZ_qc.to_instruction()

    # Combine subcircuits into a single multiqubit gate representing a single trotter step
    num_qubits = 3
    Trot_qr = QuantumRegister(num_qubits)
    Trot_qc = QuantumCircuit(Trot_qr, name='Trot')
    for i in range(0, num_qubits - 1):
        Trot_qc.append(ZZ, [Trot_qr[i], Trot_qr[i+1]])
        Trot_qc.append(YY, [Trot_qr[i], Trot_qr[i+1]])
        Trot_qc.append(XX, [Trot_qr[i], Trot_qr[i+1]])
    # Convert custom quantum circuit into a gate
    self.Trot_gate = Trot_qc.to_instruction()

  def trotterized_time_evolution(self):
    qr = QuantumRegister(7)
    qc = QuantumCircuit(qr)
    qc.x([3,5])  
    for _ in range(self.trotter_steps):
        qc.append(self.Trot_gate, [qr[1], qr[3], qr[5]])
    qc = qc.bind_parameters({self.t: self.time/self.trotter_steps})
    self.st_qcs = state_tomography_circuits(qc, [qr[1], qr[3], qr[5]])
    self.st_qcs[-1].draw()  
    
  def run_quantum(self):
    '''
    Main method to run the quantum simulation.
    '''
    backend = sim_noisy_jakarta
    self.jobs = []
    for _ in range(self.reps):
        job = execute(self.st_qcs, backend, shots=self.shots)
        print('Job ID', job.job_id())
        self.jobs.append(job)
    for job in self.jobs:
        job_monitor(job)
        try:
            if job.error_message() is not None:
                print(job.error_message())
        except:
            pass
          
  def state_tomo(self, result):
      target_state = (One^One^Zero).to_matrix()  
      tomo_fitter = StateTomographyFitter(result, self.st_qcs)
      rho_fit = tomo_fitter.fit(method='lstsq')
      fid = state_fidelity(rho_fit, target_state)
      return fid

  def fake_fidelity(self):
    self.quantum_circuit()
    self.trotterized_time_evolution()
    self.run_quantum()
    fids = []
    for job in self.jobs:
        fid = self.state_tomo(job.result())
        fids.append(fid)
    print('\nState tomography fidelity on fake Jakarta backend = {:.4f} \u00B1 {:.4f}'.format(np.mean(fids), np.std(fids)))
  
  def real_fidelity(self):
    backend = jakarta
    print(f'\nState tomography fidelity on real Jakarta backend: {self.message}') 
          
if __name__ == "__main__":
  import math
  qsim=QuantumSimulation(trotter_steps=8, target_time=math.pi, reps=8, nshots=8192)
  qsim.fake_fidelity()
  qsim.real_fidelity()