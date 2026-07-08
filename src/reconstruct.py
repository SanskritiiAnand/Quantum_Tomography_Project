from qiskit.quantum_info import DensityMatrix

def wait_for_analysis(experiment_data):
    """
    Ensure experiment execution and analysis are complete
    """
    experiment_data.block_for_results()
    return experiment_data

def get_analysis_table(experiment_data):
    """
    Return the full analysis results table as a dataframe-like object. Useful for inspection and debugging.
    """
    return experiment_data.analysis_results(dataframe= True)

def get_fitted_state_result(experiment_data):
    """
    Return the fitted state analysis result object. 
    """
    return experiment_data.analysis_results("state")

def get_reconstructed_densitymatrix(experiment_data):
    """
    Return the reconstructed state as a density matrix
    """
    state_result= get_fitted_state_result(experiment_data)
    reconstructed_state= state_result.value

    if isinstance(reconstructed_state, DensityMatrix):
        return reconstructed_state
    
    return DensityMatrix(reconstructed_state)