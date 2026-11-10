# Quantum Measurement, Tomography, and Readout Calibration
This repository implements a staged workflow for reconstructing and validating quantum states from measurement outcomes using Qiskit. It studies how quantum state tomography behaves under ideal and noisy conditions, how readout calibration is characterised through assignment matrices, and how calibration-informed reconstruction improves fidelity relative to unmitigated noise tomography.

## Project Overview
The central goal of the project is to answer a practical quantum information question:
*Given only measurement outcomes, how accurately can a prepared quantum state be reconstructed, and how does readout calibration affect the quality of that reconstruction?*
The repository approaches this through a four-staged pipeline that begins with ideal single-qubit and bell-state tomography, then introduces computational-basis readout calibration and noisy-backend comparisons. The final stage uses Qiskit Experiments' MitigatedStateTomography to evaluate reconstruction under readout-error mitigation.

## Methodology
This project follows a four-stage workflow implemented through seven modules and a main entry point(main.py). The architecture is built around state preparation, execution, reconstruction, metric evaluation, readout calibration, and visualization.
Quantum state tomography reconstructs density matrices, while fidelity, purity, and trace metrics evaluate reconstruction quality. Computational-basis assignment matrices characterize readout behaviour in Stage 3, while Stage 4 uses Qiskit Experiments' MitigatedStateTomography for calibration-informed reconstruction.

At a high level, the repository proceeds as follows:
+ Prepare known target states.
+ Run tomography circuits on an ideal or noisy simulator
+ Reconstruct the density matrix from measurement data.
+ Evaluate fidelity, purity, and trace against the reference state.
+ Build readout calibration circuits and assignment matrices.
+ Compare ideal, noisy, and readout-mitigated reconstructions in the final stage using Qiskit Experiments.

## Experimental Stages
### Stage 1: Single-qubit Tomography
Performs quantum state tomography for six known single-qubit states on an ideal simulator. The outputs from this stage include reconstructed density matrices for all six states and a fidelity bar chart summarizing reconstruction quality across the single-qubit set.
The 6 target states are: 
* $|0\rangle$
* $|1\rangle$
* $|+\rangle$
* $|-\rangle$
* $|+i\rangle$
* $|-i\rangle$

This stage establishes the baseline tomography pipeline in the absence of hardware noise, allowing the reconstruction and visualization workflow to be validated first under ideal conditions.

### Stage 2: Bell-state Tomography
Extends the tomography workflow to two-qubit entangled states on an ideal simulator. It reconstructs the density matrices of four known Bell states and produces individual density-matrix visualizations and a summary fidelity bar chart.
The 4 bell-states studies are:
* $|\Phi^+\rangle$
* $|\Phi^-\rangle$
* $|\Psi^+\rangle$
* $|\Psi^-\rangle$

This stage tests whether the same reconstruction pipeline remains reliable when moving from single-qubit states to entangled two-qubit states.

### Stage-3: Readout Calibration
Performs computational-basis readout calibration for both single-qubit and two-qubit systems using an ideal simulator. Calibration circuits are generated for every computational-basis state, and measurement counts are converted into probability vectors to construct assignment matrices. The assignment matrices characterize the conditional probabilities of measuring each basis state given a prepared basis state. The stage also calculates average assignment fidelity and produces assignment-matrix heatmaps for both systems. 
Since the calibration circuits are executed on an ideal simulator, the resulting assignment matrices are expected to be identity matrices, corresponding to ideal readout behaviour. This stage validates the custom assignment-matrix construction and readout--characterization workflow rather than demonstrating noisy readout mitigation.

### Stage 4: Ideal vs Noisy vs Calibration-informed Tomography
Introduces a noisy backend simulator based on the 127-qubit IBM Brisbane (FakeBrisbane) and performs comparative quantum state tomography. For selected single-qubit states and two-qubit Bell states, the reconstruction results are evaluated under three conditions: ideal, noisy, and readout-mitigated. The ideal and noisy branched use Qiskit Experiments' StateTomography, while the calibrated branch uses MitigatedStateTomography to incorporate readout-error mitigation into the tomography workflow. This provides a comparison of reconstructed-state fidelity and purity under different simulation conditions.
The Stage 4 mitigation workflow is implemented separately from the custom assignment-matrix calibration developed in Stage 3. It uses Qiskit's built-in mitigated tomography rather than directly applying the pseudoinverse mitigation matrix constructed in the custom calibration module.
This stage produces: 
+ Individual fidelity comparison bar charts for each selected state.
+ A combined Stage 4 fidelity summary bar chart covering the selected states and execution branches.
+ Reconstructed density-matrix plots for the ideal, noisy, and calibrated branches.

This final stage connects the earlier idealised validation pipeline to a noisy simulation environment and evaluates the effect of readout-error mitigation on reconstructed quantum states. The ideal, noisy, and calibrated branches are compared using state fidelity, reconstructed-state purity, and trace. In the tested configurations, the mitigated branch demonstrates improved reconstruction quality relative to the unmitigated noisy branch. Readout mitigation is intended to reduce measurement-induced errors, although its effectiveness depend on the noise characteristics and experimental conditions.

## Outputs
The repository generates several categories of outputs across the four stages:
### Output type	        Description
Density matrices	      Reconstructed density-matrix plots for single-qubit & Bell-state tomography, and Stage 4 comparisons.
Fidelity bar charts	    Stage-level fidelity summaries for single-qubit and Bell-state tomography.
Assignment matrices	    Computational-basis readout assignment matrices for one-qubit and two-qubit systems, accompanied by                                calibration heatmaps and assignment-fidelity metrics.
Comparison charts	      Ideal vs noisy vs calibrated fidelity comparisons in Stage 4.
Summary plots	          Final Stage 4 summary fidelity bar charts for single-qubit and Bell-state cases.

These outputs make the project interpretable both numerically and visually, with fidelity capturing agreement with the reference state, purity characterizing the mixedness of the reconstructed state, trace indicating normalization, and density matrix visualizations revealing revealing the structure of the reconstructed quantum state.

## Repository Structure
The repository structurr is organized around state preparation, execution, reconstruction, metric evaluation, readout calibration, visualisation, and the main entry point.

Quantum_Tomography_Project

├── main.py

├── src/

│   ├── calibration.py

│   ├── config.py

│   ├── executor.py

│   ├── metrics.py

│   ├── reconstruct.py

│   ├── states.py

│   └── visualize.py

└── results/
    ├── figures/

## Usage
The repository is executed through *main.py*, which uses Python's *argparse* module to select the experimental stage.
Run the following commands from the repository's root directory:
* Stage 1: python main.py --stage 1
* Stage 2: python main.py --stage 2
* Stage 3: python main.py --stage 3
* Stage 4: python main.py --stage 4 --num_qubits <"1" or "2"> --target_states <"enter the name of the state based on qubits, like "plus" or "psi_minus">

## Interpretation
### Ideal Stages
Establish the baseline expectation for quantum state tomography when backend noise is absent. High fidelity, near-unit purity, and normalized trace values indicate successful reconstruction under ideal simulation conditions. 
### Stage 4 noisy branch
Demonstrates how backend noise, including readout errors, affects the reconstructed quantum states. Changes in fidelity and purity indicate degradation in reconstruction quality relative to the ideal branch.

### Calibrated branch
Uses Qiskit Experiments' MitigatedStateTomography to incorporate readout-error mitigation inot the tomography workflow. The resulting fidelity and purity metrics are compared with the unmitigated noisy branch to evaluate the effectiveness of mitigation.

In practical terms, the project demonstrates three things:
* Quantum state tomography can accurately reconstruct known single-qubit and entangled two-qubit atates under ideal simulation conditions.
* Backend noise can reduce the quality of reconstructed quantum states.
* Readout-error mitigation can improve reconstruction quality relative to unmitigated noisy tomography under the tested simulation conditions.

Stage 3 separately demonstrates the construction and characterization of computational-basis assignment matrices using a custom implementation. Its ideal-simulator results validate the assignment-matrix workflow but do not independently demonstrate noisy readout correction.

## Limitations
This repository is a simulation-based project, not a direct hardware study. The FakeBrisbane noisy-backend workflow is valuable for studying realistic reconstruction behavior, but it is not equivalent to execution on real quantum hardware.

The custom assignment-matrix calibration implemented in stage 3 characterizes computational-basis readout behaviour, while stage 4 uses Qiskit Experiments' built-in MitigatedStateTomography. These approaches focus on readout-error characterization and mitigation rather than full fault-tolerant quantum error correction. The calibrated branch therefore cannot be interpreted as a complete solution to all quantum noise sources, and improvements observed in simulation should not be assumed to translate directly to real quantum hardware.

## Future Work
Possible extensions include:
* running the pipeline on real hardware
* adding multi-qubit states beyond Bell pairs
* expanding the metric set with eigenvalue diagnostics
* increasing automation for experiment logging and report generation
* integrating more advanced tomography or error-mitigation workflows
