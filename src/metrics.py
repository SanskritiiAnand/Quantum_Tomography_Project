import numpy as np
from qiskit.quantum_info import DensityMatrix, state_fidelity, purity

def ensure_density_matrix(state):
    """
    Convert an input quantum state to a DensityMatrix if needed
    """
    if isinstance(state, DensityMatrix):
        return state
    return DensityMatrix(state)

def compute_state_fidelity(reconstructed_state, reference_state):
    """
    Compute fidelity between reconstructed and reference states
    """
    rho_reconstructed = ensure_density_matrix(reconstructed_state)
    rho_reference = ensure_density_matrix(reference_state)

    return state_fidelity(rho_reconstructed, rho_reference)

def compute_purity(state):
    """
    Compute purity Tr(rho^2) of a quantum state
    """
    rho = ensure_density_matrix(state) 
    return purity(rho)

def compute_trace(state):
    """
    Compute Tr(rho) (should be close to 1 for a valid density matrix)
    """
    rho= ensure_density_matrix(state)
    return np.trace(rho.data)

def summarize_state_metrics(reconstructed_state, reference_state):
    """
    Return a dictionary of basic tomography metrics
    """
    rho_reconstructed = ensure_density_matrix(reconstructed_state)
    rho_reference = ensure_density_matrix(reference_state)

    return {"fidelity": compute_state_fidelity(rho_reconstructed, rho_reference),
            "purity_reconstructed": compute_purity(rho_reconstructed),
            "purity_reference": compute_purity(rho_reference),
            "trace_reconstructed": compute_trace(rho_reconstructed),
            "trace_reference": compute_trace(rho_reference)
           }