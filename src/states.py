from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, DensityMatrix

def single_qubit_state(state_name: str):
    """
    Return: 
    Circuit: QuantumCircuit that prepares the target state
    reference_statevector: iodeal Statevector of the prepared state
    reference_densitymatrix: ideal DensityMatrix of the prepared state
    Supported States: |0>, |1>, |+>, |->, |i>, |-i>
    """
    qc= QuantumCircuit(1)

    if state_name== "zero":
        pass
    elif state_name == "one":
        qc.x(0)
    elif state_name== "plus":
        qc.h(0)
    elif state_name== "minus":
        qc.x(0)
        qc.h(0)
    elif state_name== "iplus":
        qc.h(0)
        qc.s(0)
    elif state_name== "iminus":
        qc.h(0)
        qc.sdg(0)
    else:
        raise ValueError(f"Unsupported single qubit state '{state_name}'. Choose from: zero, one, plus, minus, iplus, iminus")

    ref_sv= Statevector.from_instruction(qc)
    ref_dm= DensityMatrix(ref_sv)

    return qc, ref_sv, ref_dm

def bell_state(state_name: str):
    """
    Return: 
    circuit: QuantumCircuit that prepares the bell state
    reference_statevector: ideal Statevector
    referemce_densitymatrix: ideal DensityMatrix
    Supported states: 
    Supported states: "phi_plus"   -> (|00> + |11>) / sqrt(2)
                      "phi_minus"  -> (|00> - |11>) / sqrt(2)
                      "psi_plus"   -> (|01> + |10>) / sqrt(2)
                      "psi_minus"  -> (|01> - |10>) / sqrt(2)
    """
    qc= QuantumCircuit(2)
    #start from |phi+>
    qc.h(0)
    qc.cx(0,1)

    if state_name == "phi_plus":
        pass
    elif state_name == "phi_minus":
        qc.z(0)
    elif state_name == "psi_plus":
        qc.x(1)
    elif state_name == "psi_minus":
        qc.x(1)
        qc.z(0)
    else:
        raise ValueError(f"Unsupported Bell state '{state_name}'"
                          "Choose from: phi_plus, phi_minus, psi_plus, psi_minus")
    
    ref_sv = Statevector.from_instruction(qc)
    ref_dm = DensityMatrix(ref_sv)

    return qc, ref_sv, ref_dm
