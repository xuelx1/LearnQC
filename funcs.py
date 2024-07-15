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
    operations = list(qc.data)
    i = 0  
    while i < len(operations) - 1:  
        # check if the current and next operations are both X gates and have the same target qubit 
        if (operations[i].name == 'x' and operations[i+1].name == 'x' and  
                operations[i].qargs == operations[i+1].qargs):  
            # delete these 2 gates 
            del operations[i:i+2]   
        else:  
            # otherwise, move to the next operation  
            i += 1
    new_qc = QuantumCircuit.from_qasm_str(qc.qasm())  
    new_qc.data = operations  
      
    return new_qc 
