'''
常用函数
'''
from qiskit_ibm_runtime.fake_provider import FakeProvider
from qiskit import transpile

def execute_qc(qc):
    '''
    使用模拟器执行量子程序
    '''
    backend = FakeProvider().get_backend('fake_ourense')
    new_qc = transpile(qc, backend)
    job = backend.run(new_qc)
    result = job.result()
    return result.get_counts()