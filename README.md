# Quantum Measurement, Tomography, and Readout Calibration
This repository implements a staged workflow for reconstructing and validating quantum states from measurement outcomes using Qiskit. It studies how quantum state tomography behaves under ideal and noisy conditions, how readout calibration is characterised through assignment matrices, and how calibration-informed reconstruction improves fidelity relative to unmitigated noise tomography.

## Project Overview
The central goal of the project is to answer a practical quantum information question:
*Given only measurement outcomes, how accurately can a prepared quantum state be reconstructed, and how does readout calibration affect the quality of that reconstruction?*
The repository approaches this through a four-staged pipeline that begins with ideal single-qubit and bell-state tomography, then introduces readout calibration and noisy-backend comparisons.

## Methodology
This project follows a four-stage, eight-module architecture built around preparation, execution, reconstruction, metric evaluation, and visualization.
Across the stages, the workflow uses quantum state tomography to reconstruct density matrices, fidelity, purity, and trace metrics to evaluate reconstruction quality, and assignment matrices to characterize readout behaviour.

At a high level, the repository proceeds as follows:
+ Prepare known target states.
+ Run tomography circuits on an ideal or noisy simulator
+ Reconstruct the density matrix from measurement data.
+ Evaluate fidelity, purity, and trace against the reference state.
+ Build readout calibration circuits and assignment matrices.
+ Compare ideal, noisy, and calibration-informed reconstructions in the final stage.

## Experimental Stages
### Stage-1: Single-qubit Tomography
Performs quantum state tomography for six known single-qubit states on an ideal simulator. The outputs from this stage include reconstructed density matrices for all six states and a fidelity bar chart summarizing reconstruction quality across the single-qubit set.
The 6 target states are: 
* |0>
* |1>
* |+>
* |->
* |i+>
* |i->

This stage establishes the baseline tomography pipeline in the absence of hardware noise, allowing the reconstruction and visualization workflow to be validated first under ideal conditions.

### Stage-2: Bell-state Tomography
Extends the tomography workflow to two-qubit entanngled states pon an ideal simulator. It reconstructs the density matrices of four known bell states and produces a summary fidelity bar chart and reconstructed density matrices.
The 4 bell-states studies are:
* ∣ϕ+⟩
* ∣ϕ−⟩
* ∣ψ+⟩
* ∣𝜓−⟩

This stage tests whether the same reconstruction pipeline remains reliable when moving from single-qubit states to entagled two-qubit states.

### Stage-3: Readout Calibration
Performs readout calibration for both the single-qubit and two-qubit cases on an ideal simulator. The main outputs are assignment matrices for the 1-qubit and 2-qubit systems, along with the corresponding calibration visualizations.

### Stage-4: Ideal vs Noisy vs Calibration-informed Tomography
Introduces a noisy backend simulator, the 127-qubit IBM Brisbane (FakeBrisbane), into the project and performs the final comparative analysis. For both single-qubit states and Bell states, tomography is run under ideal conditions, noisy conditions, and a calibration-informed or mitigated workflow so that the resulting fidelities can be compared directly. Qiskit Experiments provides tomography and mitigated tomography workflows that support this kind of reconstruction-and-comparison pipeline.
This stage produces: 
+ comparison bar charts for the six single-qubit states
+ comparison bar charts for the four Bell states
+ a fidelity summary bar chart for two cases each
+ density-matrix plots for ideal, noisy, and calibrated reconstructions.

This is the final stage of the repository because it connects the earlier idealized validation pipeline to a more realistic noisy-setting evaluation and shows how calibration-informed tomography recovers reconstruction quality relative to the noisy branch. Readout-mitigated tomography is specifically intended to reduce measurement-induced distortion in reconsrtucted states.

## Outputs
The repository generates several categories of outputs across the four stages:

| Output type         | Description                                                                                                |
| ------------------- | ---------------------------------------------------------------------------------------------------------- |
| Density matrices    | Reconstructed density-matrix plots for single-qubit, Bell-state, calibration, and Stage 4 comparison runs. |
| Fidelity bar charts | Stage-level fidelity summaries for single-qubit and Bell-state tomography.                                 |
| Assignment matrices | Readout calibration matrices for one-qubit and two-qubit systems.                                          |
| Comparison charts   | Ideal vs noisy vs calibrated fidelity comparisons in Stage 4.                                              |
| Summary plots       | Final Stage 4 summary fidelity bar charts for single-qubit and Bell-state cases.                           |

These outputs are  meant to make the project interpretable both numerically and visually, with fidelity capturing agreement with the reference state and density matrices revealing the structre of the reconstructed quantum state.

## Repository Structure
A typical repository structre for this project is organized around state preparation, execution, reconstruction, metrics, calibration, visualisation, and the main entrypoint.

Quantum_Tomography_project

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

## Usage
The repository is run through *main.py*, with a command-line stage selector that chooses which part of the project to execute. Python's *argparse* module is designed for this kind of staged command-line interface.
Run this command to execute the project stages:
* stage 1: python main.py --stage 1
* stage 2: python main.py --stage 2
* stage 3: python main.py --stage 3
* stage 4: python main.py --stage 4 --num_qubits <"1 or 2"> --target_states <"enter the name of the state based on qubits, like "plus" or "psi_minus">

## Interpretation
Ideal stages- provide the baseline expectation for tomography when no backend noise is present to distort results.

Stage 4 noisy branch- shows how fidelity and purity degrade when readout effects and backend noise distort the measurement statistics

Calibrated branch- demonstrates how calibration-informed tomography can recover a substantial portion of that lost accuracy. 

In practical terms, the project is designeed to ahow three things:
+ tomography can accuratelt reconstruct known states under ideal conditions
+ noise reduces the quality of reconstructed states
+ calibration-informed or mitigated tomography improves reconstruction relative to the uncorrected noisy case.

## Limitations
This repository is a simulation-based project, not a direct hardware study. The FakeBrisbane noisy-backend workflow is valuable for studying realistic reconstruction behavior, but it is not equivalent to execution on real quantum hardware.

The calibration and mitigation logic is focused on readout effects rather than full fault-tolerant error correction. As a result, the calibrated branch cannot be interpreted as a complete solution to all quantum noise sources.

## Future Work
Possible extensions include:
* running the pipeline on real hardware
* adding multi-qubit states beyond Bell pairs
* exapnding the metric set with eigenvalue diagnostics
* increasing automation for experiment logging and report generation
* integrating more advanced tomography or error-mitigation workflows
