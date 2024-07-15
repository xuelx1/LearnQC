'''
frequently used functions
'''
from qiskit_ibm_runtime.fake_provider import FakeProvider
from qiskit import transpile
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit

def execute_qc(qc):
    '''
    using simulator to execute qc
    '''
    backend = AerSimulator()
    new_qc = transpile(qc, backend)
    job = backend.run(new_qc)
    result = job.result()
    return result.get_counts()

def optimize_qc(qc):
    '''
    simple optimizations of quantum circuit
    1. remove double x gate
    '''
    # remove double x gate
    i = 0  
    while (i < len(qc.data) - 1):  
        # check if the current and next operations are both X gates and have the same target qubit 
        if ((qc.data[i].operation.name == 'x') and (qc.data[i+1].operation.name == 'x') and (qc.data[i].qubits[0]._index == qc.data[i+1].qubits[0]._index)):  
            del qc.data[i:i+2]   
        else:  
            # otherwise, move to the next operation  
            i += 1 
    return qc 
