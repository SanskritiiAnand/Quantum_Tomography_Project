from src.states import single_qubit_state
from src.executor import run_state_tomography
from src.reconstruct import (wait_for_analysis, get_reconstructed_densitymatrix, get_analysis_table)
from src.metrics import summarize_state_metrics
from src.visualize import densitymatrix_plot, fidelity_barchart

def main():
    test_states = ["zero", "one", "plus", "minus", "iplus", "iminus"]
    summary_rows = []
    for state_name in test_states:
        print("\n" + "=" * 60)
        print(f"Target state: {state_name}")

       #prepare the target state
        prep_ckt, reference_statevector, reference_densitymatrix= (single_qubit_state(state_name))

        print("\nPreparation circuit:")
        print(prep_ckt.draw(output="text"))

       #run tomography
        experiment, experiment_data= run_state_tomography(prep_ckt= prep_ckt, target_state= reference_statevector)

       #wait for analysis to complete 
        wait_for_analysis(experiment_data)

       #reconstruct density matrix
        reconstructed_densitymatrix= get_reconstructed_densitymatrix(experiment_data)

       #compute metrics
        metrics= summarize_state_metrics(reconstructed_state= reconstructed_densitymatrix, reference_state= reference_densitymatrix)

       #print outputs
        print("\nReconstructed density matrix:")
        print(reconstructed_densitymatrix.data)

        print("\nMetrics")
        print(f"fidelity: {metrics['fidelity']:.6f}")
        print(f"purity_reconstructed: {metrics['purity_reconstructed'].real:.6f}")
        print(f"purity_reference: {metrics['purity_reference'].real:.6f}")
        print(f"trace_reconstructed: {metrics['trace_reconstructed'].real:.6f}")
        print(f"trace_reference: {metrics['trace_reference'].real:.6f}")
    
        summary_rows.append({"state": state_name,
                             "fidelity": float(metrics["fidelity"]),
                             "purity_reconstructed": float(metrics["purity_reconstructed"].real),
                             "purity_reference": float(metrics["purity_reference"].real),
                             "trace_reconstructed": float(metrics["trace_reconstructed"].real),
                             "trace_reference": float(metrics["trace_reference"].real)
                           })
        
        density_plot_path= densitymatrix_plot(reconstructed_densitymatrix, state_name)
    
    print("\n" + "=" * 60)
    print("Validation Summary")
    print("=" * 60)
    for row in summary_rows:
        print(
            f"{row['state']:>8} | "
            f"fidelity = {row['fidelity']:.6f} | "
            f"purity_rec = {row['purity_reconstructed']:.6f} | "
            f"trace_rec = {row['trace_reconstructed']:.6f}"
        )
    
    fidelity_plot_path = fidelity_barchart(summary_rows)
    
    print("Saving figures into:", density_plot_path.parent)

if __name__ == "__main__":
    main()