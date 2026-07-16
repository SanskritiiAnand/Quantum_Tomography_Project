import numpy as np
from qiskit.quantum_info import DensityMatrix, state_fidelity, purity
from src.calibration import computational_basis_labels

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

    return {"fidelity": float(np.real(compute_state_fidelity(rho_reconstructed, rho_reference))),
            "purity_reconstructed": float(np.real(compute_purity(rho_reconstructed))),
            "purity_reference": float(np.real(compute_purity(rho_reference))),
            "trace_reconstructed": float(np.real(compute_trace(rho_reconstructed))),
            "trace_reference": float(np.real(compute_trace(rho_reference)))
           }

def compute_assignment_fidelity(assignment_matrix):
    """
    Average of the diagonal entries for the single-qubit assignment matrix.
    """
    if assignment_matrix.ndim != 2 or assignment_matrix.shape[0] != assignment_matrix.shape[1]:
        raise ValueError("assignment_matrix must be a square matrix")
    
    return float(np.trace(assignment_matrix) / (assignment_matrix.shape[0]))

def summarize_assignment_metrics(assignment_matrix, num_qubits):
    """
    Return a dictionary of basic readout calibration metrics
    """
    labels= computational_basis_labels(num_qubits)
    
    metrics= {}
    for i, label in enumerate(labels):
        metrics[f"P({label}|{label})"] = float(assignment_matrix[i, i])

    metrics["assignment_fidelity"] = compute_assignment_fidelity(assignment_matrix)
    return metrics

def summarize_branch_metrics(branch_name, reconstructed_state, reference_state):
    """
    Return metrics for a single stage 4 branch
    """
    metrics= summarize_state_metrics(reconstructed_state, reference_state)
    metrics["branch"]= branch_name
    return metrics

def compare_metrics(reference_state, ideal_state=None, noisy_state=None, calibrated_state=None):
    """
    Compare tomography metrics across ideal, noisy, and calibrated branches and return a dictionary keyed by branch name
    """
    comparison= {}
    if ideal_state is not None:
        comparison["ideal"]= summarize_state_metrics(ideal_state, reference_state)

    if noisy_state is not None:
        comparison["noisy"]= summarize_state_metrics(noisy_state, reference_state)

    if calibrated_state is not None:
        comparison["calibrated"]= summarize_state_metrics(calibrated_state, reference_state)

    return comparison
