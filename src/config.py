from dataclasses import dataclass, field
from pathlib import Path
from typing import List

@dataclass
class experiment_config:
    repo_name: str = "repo3-Quantum Tomography"

    #execution settings
    shots: int= 4096
    seed_simulator: int= 42

    #backend mode: "ideal" or "noisy"
    backend_mode: str= "ideal"

    #fitter choice (tomography analysis)
    fitter: str= "linear_inversion"

    #project scope
    stage: int= 1 
    num_qubits: int= 1 
    target_states: List[str]= field(default_factory=lambda: ["plus"])

    #calibration/mitigation flags
    enable_readout_calibration: bool=False
    enable_noise_model: bool=False

    #paths
    project_root: Path= Path(__file__).resolve().parent.parent
    src_dir: Path= field(init= False)
    results_dir: Path= field(init= False)
    figures_dir: Path= field(init= False)
    data_dir: Path= field(init= False)

    def post_init(self):
        self.src_dir = self.project_root / "src"
        self.results_dir = self.project_root / "results"
        self.figures_dir = self.results_dir / "figures"
        self.data_dir = self.results_dir / "data"

        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.figures_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        valid_backend_modes = ("ideal", "noisy")
        valid_fitters = { "linear_inversion"}

        if self.backend_mode not in valid_backend_modes:
            raise ValueError(f"Invalid backend mode '{self.backend_mode}'."
                             f"Choose from {valid_backend_modes}")
        
        if self.fitter not in valid_fitters:
            raise ValueError(f"Invalid fitter '{self.fitter}'."
                             f"Choose from {valid_fitters}.")
        
        if self.stage not in {1, 2, 3, 4}:
            raise ValueError("Stage must be one of {1, 2, 3, 4}")
        
        if self.num_qubits < 1:
            raise ValueError("num_qubits must be at least 1")
        
CONFIG = experiment_config