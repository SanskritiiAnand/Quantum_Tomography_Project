import argparse
from src.states import single_qubit_state, bell_state
from src.executor import run_state_tomography, run_circuits, run_mitigated_state_tomography
from src.reconstruct import (wait_for_analysis, get_reconstructed_densitymatrix)
from src.metrics import summarize_state_metrics, summarize_assignment_metrics, compare_metrics
from src.visualize import densitymatrix_plot, fidelity_barchart, assignment_matrix_heatmap, fidelity_comparison
from src.config import CONFIG
from src.calibration import (build_basis_calibration, build_assignment_matrix, assignment_matrix_dataframe)

def set_execution_mode(backend_mode, enable_noise_model=False, enable_readout_calibration=False, enable_mitigation=False):
    CONFIG.backend_mode= backend_mode
    CONFIG.enable_noise_model= enable_noise_model
    CONFIG.enable_readout_calibration= enable_readout_calibration
    CONFIG.enable_mitigation= enable_mitigation

def run_tomography_suite(state_names, state_builder, suite_label):
    summary_rows= []
    last_density_plot_path= None

    print("\n" + "=" * 60)
    print(f"{suite_label}")
    print("=" * 60)

    for state_name in state_names:
        print("\n" + "=" * 60)
        print(f"Target state: {state_name}")

        prep_ckt, reference_sv, reference_dm= state_builder(state_name)

        print("\nPreparation circuit:")
        print(prep_ckt.draw(output="text"))

        experiment, experiment_data= run_state_tomography(prep_ckt=prep_ckt, target_state=reference_sv)

        wait_for_analysis(experiment_data)

        reconstructd_dm= get_reconstructed_densitymatrix(experiment_data)

        metrics= summarize_state_metrics(reconstructed_state= reconstructd_dm, reference_state= reference_dm)

        print("\nReconstructed density matrix:")
        print(reconstructd_dm.data)

        print("\nMetrics")
        print(f"fidelity: {metrics['fidelity']:.6f}")
        print(f"purity_reconstructed: {metrics['purity_reconstructed']:.6f}")
        print(f"purity_reference: {metrics['purity_reference']:.6f}")
        print(f"trace_reconstructed: {metrics['trace_reconstructed'].real:.6f}")
        print(f"trace_reference: {metrics['trace_reference'].real:.6f}")

        summary_rows.append({"state": state_name, 
                             "fidelity": float(metrics["fidelity"]), 
                             "purity_reconstructed": float(metrics["purity_reconstructed"]),
                             "purity_reference": float(metrics["purity_reference"]),
                             "trace_reconstructed": float(metrics["trace_reconstructed"].real),
                             "trace_reference": float(metrics["trace_reference"].real)
                            })
        last_density_plot_path= densitymatrix_plot(reconstructd_dm, state_name)

    return summary_rows

def print_summary(summary_rows, heading):
    print("\n"+"="*60)
    print(heading)
    print("="*60)

    for row in summary_rows:
        print(f"{row['state']:>10} |"
              f"fidelity= {row['fidelity']:.6f} |"
              f"purity_rec= {row['purity_reconstructed']:.6f} |"
              f"trace_rec= {row['trace_reconstructed']:.6f}"
             )
        
def run_single_qubit():
    test_states = ["zero", "one", "plus", "minus", "iplus", "iminus"]

    set_execution_mode(backend_mode="ideal", enable_noise_model=False, 
                       enable_readout_calibration=False, enable_mitigation=False)
    
    summary_rows, last_density_plot_path = run_tomography_suite(state_names= test_states, 
                                                                state_builder= single_qubit_state, 
                                                                suite_label="Stage 1: Single-qubit tomography")
    fidelity_plot_path= fidelity_barchart(summary_rows, 
                                          title="Single-qubit state tomography fidelity", 
                                          filename="single_qubit_fidelity.png")
    
    print_summary(summary_rows, "Validation Summary: Single-qubit States")
    print("saving figures into:", fidelity_plot_path.parent)

def run_bell_state():
    bell_states= ["phi_plus", "phi_minus", "psi_plus", "psi_minus"]

    set_execution_mode(backend_mode="ideal", enable_noise_model=False, 
                       enable_readout_calibration=False, enable_mitigation=False)
    
    summary_rows, last_density_plot_path= run_tomography_suite(state_names= bell_states, 
                                                               state_builder= bell_state, 
                                                               suite_label= "Stage  2: Bell-state tomography")
    fidelity_plot_path= fidelity_barchart(summary_rows, 
                                          title="Bell-state tomography fidelity", 
                                          filename="bell_state_fidelity.png")
    
    print_summary(summary_rows, "Validqation Summary: Bell states")
    print("saving figures into:", fidelity_plot_path.parent)

def print_assignment_metrics(assignment_matrix, num_qubits):
    metrics= summarize_assignment_metrics(assignment_matrix, num_qubits=num_qubits)

    print("\nMetrics")
    for key, value in metrics.items():
        print(f"{key}: {value:.6f}")

def run_calibration_case(num_qubits, label):
    print("\n" + "=" * 60)
    print(label)
    print("=" * 60)

    circuits = build_basis_calibration(num_qubits=num_qubits)

    print("\nCalibration Circuits:")
    for state_label, circuit in circuits.items():
        print(f"\nPrepared state: {state_label}")
        print(circuit.draw(output="text"))

    counts_dict = run_circuits(circuits, shots=CONFIG.calibration_shots)

    print("\nCounts:")
    for state_label, counts in counts_dict.items():
        print(f"{state_label}: {counts}")

    assignment_matrix = build_assignment_matrix(counts_dict, num_qubits=num_qubits)
    assignment_df = assignment_matrix_dataframe(assignment_matrix, num_qubits=num_qubits)

    print("\nAssignment Matrix:")
    print(assignment_df)

    print_assignment_metrics(assignment_matrix, num_qubits=num_qubits)

    heatmap_path = assignment_matrix_heatmap(assignment_matrix, num_qubits=num_qubits, 
                                             title=f"{num_qubits}-qubit assignment matrix", 
                                             filename=f"assignment_matrix_{num_qubits}q.png" )
    print("\nSaving figures into:", heatmap_path.parent)

    return {"counts": counts_dict, "assignment_matrix": assignment_matrix, 
            "assignment_dataframe": assignment_df }

def run_calibration():
    print("\n" + "=" * 60)
    print("Stage 3: Readout calibration")
    print("=" * 60)

    set_execution_mode(backend_mode="ideal", enable_noise_model=False, 
                       enable_readout_calibration=True, enable_mitigation=False)

    single_qubit_results = run_calibration_case(num_qubits=1, 
                                                label="Single-qubit readout calibration")
    two_qubit_results = run_calibration_case(num_qubits=2, 
                                             label="Two-qubit readout calibration")

    return {"single_qubit": single_qubit_results, "two_qubit": two_qubit_results}

def run_stage4_state(state_name, state_builder, suite_label):
    print("\n" + "=" * 60)
    print(f"{suite_label} :: {state_name}")
    print("=" * 60)

    prep_ckt, reference_sv, reference_dm= state_builder(state_name)
    print("\nPreparation circuit:")
    print(prep_ckt.draw(output="text"))

    branch_results= {}
    calibration_results=None

    if CONFIG.run_ideal_branch:
        print("\n---Running ideal branch---")
        set_execution_mode(backend_mode="ideal", enable_noise_model=False, 
                           enable_readout_calibration=False, enable_mitigation=False)

        _, experiment_data= run_state_tomography(prep_ckt=prep_ckt, 
                                                 target_state=reference_sv, 
                                                 shots=CONFIG.tomography_shots)

        wait_for_analysis(experiment_data)
        ideal_dm= get_reconstructed_densitymatrix(experiment_data)
        branch_results["ideal"]= ideal_dm

        densitymatrix_plot(ideal_dm, f"{state_name}_ideal", 
                           title=f"Ideal reconstructed density matrix: {state_name}", 
                           filename=f"density_matrix_{state_name}_ideal.png")
    
    if CONFIG.run_noisy_branch:
        print("\n---Running noisy branch---")
        set_execution_mode(backend_mode="noisy", enable_noise_model=True, 
                           enable_readout_calibration=False, enable_mitigation=False)

        _, experiment_data= run_state_tomography(prep_ckt=prep_ckt, 
                                                 target_state=reference_sv, 
                                                 shots=CONFIG.tomography_shots)

        wait_for_analysis(experiment_data)
        noisy_dm= get_reconstructed_densitymatrix(experiment_data)
        branch_results["noisy"]= noisy_dm

        densitymatrix_plot(noisy_dm, f"{state_name}_noisy", 
                           title=f"Noisy reconstructed density matrix: {state_name}", 
                           filename=f"density_matrix_{state_name}_noisy.png")


    if CONFIG.run_calibrated_branch:
        print("\n--- Running calibration branch ---")
        set_execution_mode(backend_mode="noisy", enable_noise_model=True, 
                           enable_readout_calibration=True, enable_mitigation=True)

        _, experiment_data= run_mitigated_state_tomography(prep_ckt=prep_ckt, 
                                                           target_state= reference_sv, 
                                                           shots=CONFIG.tomography_shots)

        wait_for_analysis(experiment_data)
        calibrated_dm= get_reconstructed_densitymatrix(experiment_data)
        branch_results["calibrated"]= calibrated_dm

        densitymatrix_plot(calibrated_dm, f"{state_name}_calibrated", 
                           title=f"Calibrated reconstructed density matrix: {state_name}", 
                           filename=f"density_matrix_{state_name}_calibrated.png")

    comparison = compare_metrics(reference_state=reference_dm, 
                                 ideal_state=branch_results.get("ideal"), 
                                 noisy_state=branch_results.get("noisy"), 
                                 calibrated_state=branch_results.get("calibrated"))

    print("\nStage 4 metrics summary:")
    for branch, metrics in comparison.items():
        print(f"{branch:>10} | "
              f"fidelity= {metrics['fidelity']:.6f} | "
              f"purity_rec= {metrics['purity_reconstructed']:.6f} | "
              f"trace_rec= {metrics['trace_reconstructed'].real:.6f}"
             )
        
    comparison_plot_path = fidelity_comparison(comparison, 
                                               filename=f"stage4_fidelity_{state_name}.png", 
                                               title=f"Stage 4 Fidelity Comparison: {state_name}")

    print("\nSaved Stage 4 comparison figure to:", comparison_plot_path)
    
    return {"state_name": state_name,
            "reference_dm": reference_dm,
            "branches": branch_results,
            "comparison": comparison,
            "calibration": calibration_results,
            "comparison_plot": comparison_plot_path,
           }

def run_stage4(num_qubits=None, target_states=None):
    print("\n" + "=" * 60)
    print("Stage 4: Ideal vs noisy vs calibration-informed tomography")
    print("=" * 60)

    selected_num_qubits= num_qubits if num_qubits is not None else CONFIG.num_qubits
    selected_target_states= target_states if target_states is not None else CONFIG.target_states

    if selected_num_qubits == 1:
        state_builder = single_qubit_state
        state_names = selected_target_states or ["plus"]
        suite_label = "Single-qubit Stage 4 comparison"
    elif selected_num_qubits == 2:
        state_builder = bell_state
        state_names = selected_target_states or ["phi_plus"]
        suite_label = "Two-qubit Stage 4 comparison"
    else:
        raise ValueError("Stage 4 currently supports num_qubits = 1 or 2")

    stage4_results = []
    fidelity_rows = []

    for state_name in state_names:
        result = run_stage4_state(state_name=state_name, 
                                  state_builder=state_builder, 
                                  suite_label=suite_label)
        stage4_results.append(result)
        for branch, metrics in result["comparison"].items():
            fidelity_rows.append({"state": f"{state_name}_{branch}", 
                                  "fidelity": float(metrics["fidelity"])})

    summary_plot_path = fidelity_barchart(fidelity_rows, 
                                          title="Stage 4 fidelity summary", 
                                          filename="stage4_fidelity_summary.png")

    print("\nSaved Stage 4 summary figure to:", summary_plot_path.parent)

    return stage4_results

def parse_args():
    parser= argparse.ArgumentParser(description= "Run quantum state tomography validation suites.")
    parser.add_argument("--stage", choices=["1","2","3", "4"], required=True, help= "Choose stage 1, 2, 3 or 4")
    parser.add_argument("--num_qubits", type=int, choices= [1,2], help="Number of qubits for stage 4")
    parser.add_argument("--target_states", nargs="+", help="Target states for stage 4")

    return parser.parse_args()

def main():
    args= parse_args()
    
    if args.stage == "1":
        run_single_qubit()
    elif args.stage == "2":
        run_bell_state()
    elif args.stage == "3":
        run_calibration()
    elif args.stage == "4":
        run_stage4(num_qubits=args.num_qubits, target_states=args.target_states)

if __name__ == "__main__":
    main()
