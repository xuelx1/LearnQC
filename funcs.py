 # * Copyright 2024 Xue_Lexiang
 # * Licensed under MIT (https://github.com/xuelx1/LearnQC/LISENCE)
'''
frequently used functions
'''
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile
import numpy as np

def execute_qc(qc):
    '''
    using simulator to execute qc
    '''
    backend = AerSimulator()
    new_qc = transpile(qc, backend)
    job = backend.run(new_qc)
    result = job.result()
    return result.get_counts()


