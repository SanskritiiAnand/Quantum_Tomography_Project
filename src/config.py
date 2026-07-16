from dataclasses import dataclass, field
from pathlib import Path
from typing import List

@dataclass
class experiment_config:
    repo_name: str = "repo3-Quantum Tomography"

    #execution settings
    shots: int= 4096
    tomography_shots: int = 4096
    calibration_shots: int= 4096
    seed_simulator: int= 42
    seed_transpiler: int=42

    #backend mode: "ideal" or "noisy"
    backend_mode: str= "ideal"
    noisy_backend: str = "FakeBrisbane"

    #fitter choice (tomography analysis)
    fitter: str= "linear_inversion"

    #project scope
    stage: int= 1 
    num_qubits: int= 1 
    target_states: List[str]= field(default_factory=lambda: ["plus"])

    #calibration/mitigation flags
    enable_readout_calibration: bool=False
    enable_noise_model: bool=False
    enable_mitigation: bool=False

    #stage 4 comparison branches
    run_ideal_branch: bool= True
    run_noisy_branch: bool= True
    run_calibrated_branch: bool= True

    #paths
    project_root: Path= Path(__file__).resolve().parent.parent
    src_dir: Path= field(init= False)
    results_dir: Path= field(init= False)
    figures_dir: Path= field(init= False)
    data_dir: Path= field(init= False)

    def __post_init__(self):
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
        
        if self.seed_simulator < 0:
            raise ValueError("seed_simulator must be non-negative")
        
        if self.seed_transpiler < 0:
            raise ValueError("seed_transpiler must be non-negative")
        
        if self.shots < 1:
            raise ValueError("shots must be at least 1")
        
        if self.tomography_shots < 1:
            raise ValueError("tomography_shots must  be at least 1")
        
        if self.calibration_shots < 1: 
            raise ValueError("calibration_shots must be at least 1")
        
        if not self.target_states:
            raise ValueError("target_states must contain at least 1 state")
        
        if self.backend_mode == "ideal" and self.enable_noise_model:
            raise ValueError("enable_noise_model cannot be True when backend_mode = 'ideal'. ")
        
        if self.enable_mitigation and not self.enable_readout_calibration:
            raise ValueError("enable_mitigation = True requires enable_readout_calibration= True")
        
        if self.stage == 4:
            if not (self.run_ideal_branch or self.run_noisy_branch or self.run_calibrated_branch):
                raise ValueError("For stage 4, at least one comparison branch  must be enabled")
            
            if self.run_calibrated_branch:
                if self.backend_mode != "noisy":
                    raise ValueError("Calibrated branch requires backend_mode = 'noisy'")
                
                if not self.enable_readout_calibration:
                    raise ValueError("calibrated branch requires enablr_readout_calibration = True")
                
                if not self.enable_mitigation:
                    raise ValueError("Calibrated branch requires enable_mitigation = True")
        
CONFIG = experiment_config()
