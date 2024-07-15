'''
frequently used functions
'''
from qiskit_ibm_runtime.fake_provider import FakeProvider
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile

def execute_qc(qc):
    '''
    using simulator to execute qc
    '''
    backend = AerSimulator()
    new_qc = transpile(qc, backend)
    job = backend.run(new_qc)
    result = job.result()
    return result.get_counts()

