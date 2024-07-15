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

def infuncs_find_next_opt(qc, idx):
    '''
    find the next optimal gate on same qubit
    '''
    if idx >= len(qc.data):
        raise ValueError('Index out of range')
    opt = qc.data[idx].operation.name
    j = 0
    while(j+idx < len(qc.data) and len(qc.data[idx+j].qubits)==1):
        if ((qc.data[idx+j].operation.name == opt) and 
            (qc.data[idx].qubits[0]._index == qc.data[idx+1].qubits[0]._index)): 
            return idx+j
        else:
            j += 1
    return idx
        
def optimize_qc(qc):
    '''
    simple optimizations of quantum circuit
    1. remove double x gate
    '''
    # remove double x gate
    i = 0  
    while (i < len(qc.data) - 1):  
        # check if the current and next operations are both X gates and have the same target qubit 
        if (qc.data[i].operation.name == 'x'):
            next = infuncs_find_next_opt(qc, i)
            print(qc.data[i].operation.name, i, next)
            if (next > i):
                del qc.data[i, next]
            else:
                i += 1
    return qc 
