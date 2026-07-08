from qiskit_aer import AerSimulator
from qiskit_experiments.library import StateTomography
from .config import CONFIG

def get_backend():
    """
    Return the backend according to the configuration
    """
    if CONFIG.backend_mode == "ideal":
        return AerSimulator(seed_simulator = CONFIG.seed_simulator)
    
    elif CONFIG.backend_mode == "noisy":
        return AerSimulator(seed_simulator = CONFIG.seed_simulator) #placeholder for stage 4
    
    else:
        raise ValueError(f"Unsupported backend_mode '{CONFIG.backend_mode}'"
                         "Choose 'ideal' or 'noisy'")
    
def build_state_tomography(prep_ckt, target_state = None):
    """
    Build a State Tomography experiment from a preparation circuit.
    """
    experiment = StateTomography(prep_ckt)
    experiment.analysis.set_options(fitter = CONFIG.fitter, target = target_state)

    return experiment

def run_state_tomography(prep_ckt, target_state = None):
    """
    Run the tomography experiment and return: experiment, experiment_data
    """
    backend = get_backend()
    experiment = build_state_tomography(prep_ckt= prep_ckt, target_state= target_state)

    experiment_data = experiment.run(backend= backend, shots= CONFIG.shots)

    return experiment, experiment_data