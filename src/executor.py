from qiskit_aer import AerSimulator
from qiskit_experiments.library import StateTomography, MitigatedStateTomography
from .config import CONFIG
from qiskit import transpile
from qiskit_ibm_runtime.fake_provider import FakeBrisbane

def _get_fake_backend():
    """
    Return the fake hardware backend selected in config
    """
    fake_backend_name= CONFIG.noisy_backend

    if fake_backend_name == "FakeBrisbane":
        return FakeBrisbane()
    
    raise ValueError(f"Unsupported noisy backend '{fake_backend_name}'. Add it to _get_fake_backend() before using")

def get_backend():
    """
    Return the backend according to the configuration
    """
    if CONFIG.backend_mode == "ideal":
        return AerSimulator(seed_simulator = CONFIG.seed_simulator)
    
    elif CONFIG.backend_mode == "noisy":
        fake_backend = _get_fake_backend()
        backend= AerSimulator.from_backend(fake_backend)
        backend.set_options(seed_simulator= CONFIG.seed_simulator)
        return backend
    
    else:
        raise ValueError(f"Unsupported backend_mode '{CONFIG.backend_mode}'"
                         "Choose 'ideal' or 'noisy'")

def run_circuit(circuit, shots=None):
    """
    Run a single circuit and return counts
    """
    backend= get_backend()
    shots= shots or CONFIG.tomography_shots

    transpiled_circuit= transpile(circuit, backend, seed_transpiler=CONFIG.seed_transpiler)
    job= backend.run(transpiled_circuit, shots=shots, seed_simulator= CONFIG.seed_simulator)
    result= job.result()
    return result.get_counts()

def run_circuits(circuits, shots=None):
    """
    Run a dictionary  of named circuits and return a dictionary of counts
    """
    output= {}
    for label, circuit in circuits.items():
        output[label]= run_circuit(circuit, shots=shots)
    return output

def build_state_tomography(prep_ckt, target_state = None):
    """
    Build a State Tomography experiment from a preparation circuit.
    """
    experiment = StateTomography(prep_ckt)
    experiment.analysis.set_options(fitter = CONFIG.fitter, target = target_state)
    experiment.set_transpile_options(seed_transpiler= CONFIG.seed_transpiler)

    return experiment

def run_state_tomography(prep_ckt, target_state = None, shots= None):
    """
    Run the tomography experiment and return: experiment, experiment_data
    """
    backend = get_backend()
    experiment = build_state_tomography(prep_ckt= prep_ckt, target_state= target_state)
    experiment.set_run_options(shots=shots or CONFIG.tomography_shots, seed_simulator= CONFIG.seed_simulator)
    experiment_data = experiment.run(backend= backend)

    return experiment, experiment_data

def build_mitigated_state_tomography(prep_ckt, target_state=None):
    experiment= MitigatedStateTomography(prep_ckt)
    experiment.analysis.set_options(fitter= CONFIG.fitter, target= target_state)
    experiment.set_transpile_options(seed_transpiler= CONFIG.seed_transpiler)

    return experiment

def run_mitigated_state_tomography(prep_ckt, target_state= None, shots=None):
    backend= get_backend()
    experiment= build_mitigated_state_tomography(prep_ckt=prep_ckt, target_state=target_state)
    experiment.set_run_options(shots=shots or CONFIG.tomography_shots, seed_simulator= CONFIG.seed_simulator)
    experiment_data= experiment.run(backend=backend)
    return experiment, experiment_data
