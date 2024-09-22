"""
Based on past Qiskit implementation : https://github.com/kazawai/shor_qiskit
"""
import traceback
# Time the execution of the algorithm
from time import time
from fractions import Fraction
from numpy import ceil, floor, log2, pi, zeros
# For shor's algorithm in qiskit version 1.0.1
from qiskit import (ClassicalRegister, QuantumCircuit, QuantumRegister,
                    transpile)
from qiskit.circuit.quantumcircuit import Qubit, QubitSpecifier

def qft(
    circuit: QuantumCircuit, qreg: QuantumRegister, n: int, with_swaps: bool = True
):
    """n-qubit QFT on q in circ."""
    for j in range(n - 1, 0, -1):
        circuit.h(qreg[j])
        for k in range(j - 1, -1, -1):
            if (pi / float(2 ** (j - k))) > 0:
                circuit.cp(pi / float(2 ** (j - k)), qreg[j], qreg[k])
        if with_swaps:
            circuit.barrier()

    if with_swaps:
        for j in range(n // 2):
            circuit.swap(qreg[j], qreg[n - j - 1])
    return circuit


def qft_dagger(
    circuit: QuantumCircuit, qreg: QuantumRegister, n: int, with_swaps: bool = True
):
    """n-qubit QFTdagger on q in circ."""
    if with_swaps:
        for j in range(n // 2):
            circuit.swap(qreg[j], qreg[n - j - 1])

    for j in range(n):
        circuit.h(qreg[j])
        if j != n - 1:
            for k in range(j, -1, -1):
                if (pi / float(2 ** ((j + 1) - k))) > 0:
                    circuit.cp(-pi / float(2 ** ((j + 1) - k)), qreg[j + 1], qreg[k])
        if with_swaps:
            circuit.barrier()
    return circuit


def get_angles(a, N):
    """Compute the angles for the QPE"""
    s = bin(int(a))[2:].zfill(N)
    angles = zeros([N])
    for i in range(0, N):
        for j in range(i, N):
            if s[j] == "1":
                angles[N - i - 1] += pow(2, -(j - i))
        angles[N - i - 1] *= pi
    return angles


def cc_phase_gate(
    circuit: QuantumCircuit,
    control_qubits: list[QubitSpecifier | Qubit | QuantumRegister],
    target_qubit: int,
    angle: float,
):
    """Create a doubly controlled phase gate"""
    if len(control_qubits) != 2:
        raise ValueError(
            "The doubly controlled phase gate needs exactly 2 control qubits"
        )

    circuit.cp(angle / 2, control_qubits[0], target_qubit)
    circuit.cx(control_qubits[1], control_qubits[0])
    circuit.cp(-angle / 2, control_qubits[0], target_qubit)
    circuit.cx(control_qubits[1], control_qubits[0])
    circuit.cp(angle / 2, control_qubits[1], target_qubit)


def phi_adder(
    circuit: QuantumCircuit,
    qreg: QuantumRegister,
    a: int,
    N: int,
    inverse: bool = False,
):
    """Create the circuit that performs the addition by a in the Fourier space (mod N)"""
    angles = get_angles(a, N)
    for i in range(N):
        if len(angles) == 0:
            break
        if not inverse:
            circuit.p(angles[i], qreg[i])
        else:
            circuit.p(-angles[i], qreg[i])


def controlled_phi_adder(
    circuit: QuantumCircuit,
    qreg: QuantumRegister,
    a: int,
    N: int,
    control_qubits: QuantumRegister | Qubit | list[Qubit],
    inverse: bool = False,
):
    """Controlled version of the phi_adder"""
    angles = get_angles(a, N)
    for i in range(N):
        if len(angles) == 0:
            break
        if not inverse:
            if (
                isinstance(control_qubits, QuantumRegister)
                or isinstance(control_qubits, Qubit)
                or len(control_qubits) == 1
            ):
                circuit.cp(
                    angles[i],
                    (
                        control_qubits
                        if isinstance(control_qubits, QuantumRegister)
                        or isinstance(control_qubits, Qubit)
                        else control_qubits[0]
                    ),
                    qreg[i],
                )

            else:
                cc_phase_gate(circuit, control_qubits, qreg[i], angles[i])
        else:
            if (
                isinstance(control_qubits, QuantumRegister)
                or isinstance(control_qubits, Qubit)
                or len(control_qubits) == 1
            ):
                circuit.cp(
                    -angles[i],
                    (
                        control_qubits
                        if isinstance(control_qubits, QuantumRegister)
                        or isinstance(control_qubits, Qubit)
                        else control_qubits[0]
                    ),
                    qreg[i],
                )
            else:
                cc_phase_gate(circuit, control_qubits, qreg[i], -angles[i])


def controlled_phi_adder_mod_N(
    circuit: QuantumCircuit,
    qreg: QuantumRegister,
    a: int,
    N: int,
    n: int,
    control_qubits: QuantumRegister | Qubit | list[Qubit],
    ancilla_qubit: Qubit,
):
    """Controlled version of the phi_adder"""
    controlled_phi_adder(circuit, qreg, a, n, control_qubits, False)
    phi_adder(circuit, qreg, N, n, True)
    qft_dagger(circuit, qreg, n, False)
    circuit.cx(qreg[n - 1], ancilla_qubit)
    qft(circuit, qreg, n, False)
    controlled_phi_adder(circuit, qreg, N, n, control_qubits, False)

    controlled_phi_adder(circuit, qreg, a, n, control_qubits, True)
    qft_dagger(circuit, qreg, n, False)
    circuit.x(qreg[n - 1])
    circuit.cx(qreg[n - 1], ancilla_qubit)
    circuit.x(qreg[n - 1])
    qft(circuit, qreg, n, False)
    controlled_phi_adder(circuit, qreg, a, n, control_qubits, False)


def controlled_phi_adder_mod_N_inv(
    circuit: QuantumCircuit,
    qreg: QuantumRegister,
    a: int,
    N: int,
    n: int,
    control_qubits: QuantumRegister | Qubit | list[Qubit],
    ancilla_qubit: Qubit,
):
    """Controlled version of the inverse phi_adder"""
    controlled_phi_adder(circuit, qreg, a, n, control_qubits, True)
    qft_dagger(circuit, qreg, n, False)
    circuit.x(qreg[n - 1])
    circuit.cx(qreg[n - 1], ancilla_qubit)
    circuit.x(qreg[n - 1])
    qft(circuit, qreg, n, False)
    controlled_phi_adder(circuit, qreg, a, n, control_qubits, False)

    controlled_phi_adder(circuit, qreg, N, n, control_qubits, False)
    qft_dagger(circuit, qreg, n, False)
    circuit.cx(qreg[n - 1], ancilla_qubit)
    qft(circuit, qreg, n, False)
    phi_adder(circuit, qreg, N, n, False)
    controlled_phi_adder(circuit, qreg, a, n, control_qubits, True)


def controlled_mult_mod_N(
    circuit: QuantumCircuit,
    qreg: QuantumRegister,
    a: int,
    N: int,
    n: int,
    control_reg: QuantumRegister | Qubit,
    ancilla_reg: QuantumRegister,
):
    """Controlled version of the multiplication by a mod N"""
    qft(circuit, ancilla_reg, n + 1, False)
    for i in range(n):
        controlled_phi_adder_mod_N(
            circuit,
            ancilla_reg,
            (2**i) * a % N,
            N,
            n + 1,
            [qreg[i], control_reg],
            ancilla_reg[n + 1],
        )
    qft_dagger(circuit, ancilla_reg, n + 1, False)

    for i in range(n):
        circuit.cswap(control_reg, qreg[i], ancilla_reg[i])

    a_inv = pow(a, -1, N)
    qft(circuit, ancilla_reg, n + 1, False)

    for i in range(n):
        controlled_phi_adder_mod_N_inv(
            circuit,
            ancilla_reg,
            pow(2, i) * a_inv % N,
            N,
            n + 1,
            [qreg[i], control_reg],
            ancilla_reg[n + 1],
        )
    qft_dagger(circuit, ancilla_reg, n + 1, False)

def qpe_period_finding(a: int, n: int, N: int, backend) -> int | str:
    """Quantum Phase Estimation for period finding"""
    q_up = QuantumRegister(2 * n, "q_up")
    q_down = QuantumRegister(n, "q_down")
    a_q = QuantumRegister(n + 2, "a_q")
    c = ClassicalRegister(2 * n, "c")
    qpe = QuantumCircuit(q_up, q_down, a_q, c)
    try:
        # Initialize qubits
        qpe.h(q_up)
        qpe.x(q_down[0])

        # Apply controlled multiplication gates
        for i in range(n):
            controlled_mult_mod_N(
                qpe, q_down, int(pow(a, pow(2, i))), N, n, q_up[i], a_q
            )

        # Apply inverse QFT
        qft_dagger(qpe, q_up, 2 * n, True)

        # Measure the qubits
        qpe.measure(q_up, c)

        # Transpile the circuit
        try:
            transpiled_qpe = transpile(qpe, backend)
        except Exception as e:
            print(traceback.format_exc())
            return "Error"

        job = backend.run(transpiled_qpe, shots=1024)
        res = job.result().get_counts()
        return res

    except Exception as e:
        print(traceback.format_exc())
        return "Error"
    
def shor_quantum(a: int, n: int, backend):
    N = int(ceil(log2(n)))
    results = qpe_period_finding(a, N, n, backend)
    if results == "Error":
        return 0
    for key,_ in results.items():
        phase_est = float(int(key, 2)) / 2**(2*n)
        frac = Fraction.from_float(phase_est).limit_denominator(N)
        r = frac.denominator
        if pow(a, r, N) == 1 and r % 2 == 0:
            return r
    return 0