from pathlib import Path
import matplotlib.pyplot as plt
from qiskit.visualization import plot_state_city
import numpy as np
from src.calibration import computational_basis_labels

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIGURES_DIR = PROJECT_ROOT / "results" / "figures"

def ensure_directory(path):
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def densitymatrix_plot(density_matrix, state_name, output_dir= FIGURES_DIR, title=None, filename=None):
    output_dir= ensure_directory(output_dir)
    plot_title= title or f"Reconstructed density matrix: {state_name}"
    fig = plot_state_city(density_matrix, title= plot_title)
    
    for ax in fig.axes:
        if hasattr(ax, 'zaxis'):
            ax.set_zlim(0.0, 1.0)
    file_path= output_dir / (filename or f"density_matrix_{state_name}.png")
    fig.savefig(file_path, dpi=200, bbox_inches="tight")
    plt.close(fig)

    return file_path

def fidelity_barchart(summary_rows, output_dir= FIGURES_DIR, title= "State Tomography Fidelity by Test State", filename= "fidelity_summary.png"):
    output_dir= ensure_directory(output_dir)

    states = [row["state"] for row in summary_rows]
    fidelities = [row["fidelity"] for row in summary_rows]

    fig, ax= plt.subplots(figsize=(8,5))
    bars= ax.bar(states, fidelities, color="steelblue")

    ax.set_title(title)
    ax.set_xlabel("State")
    ax.tick_params(axis="x", rotation= 30)
    ax.set_ylabel("Fidelity")
    ax.set_ylim(0.0, 1.05)
    ax.grid(axis="y", linestyle= "--", alpha=0.4)

    for bar, fidelity in zip(bars, fidelities):
        ax.text(bar.get_x() + bar.get_width() / 2, fidelity + 0.01, f"{fidelity:.4f}", ha="center", va="bottom", fontsize= 9)

    fig.tight_layout()
    file_path= output_dir / filename
    fig.savefig(file_path, dpi=200, bbox_inches="tight")
    plt.close(fig)

    return file_path

def assignment_matrix_heatmap(assignment_matrix, num_qubits, output_dir= FIGURES_DIR, filename= "assignment_matrix.png", title="Assignment Matrix"):
    output_dir= ensure_directory(output_dir)
    labels= computational_basis_labels(num_qubits)

    fig_size= max(5, len(labels)* 1.2)
    fig, ax= plt.subplots(figsize=(fig_size, fig_size))
    im= ax.imshow(assignment_matrix, cmap="Blues", vmin=0, vmax=1)

    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))
    ax.set_xticklabels([f"prepared {label}" for label in labels], rotation=45, ha="right")
    ax.set_yticklabels([f"measured {label}" for label in labels])
    ax.set_xlabel("Prepared state")
    ax.set_ylabel("Measured outcome")
    ax.set_title(title)

    threshold= 0.5
    for i in range(len(labels)):
        for j in range(len(labels)):
            value= assignment_matrix[i,j]
            text_color= "white" if value > threshold else "black"
            ax.text(j, i, f"{value:.4f}", ha="center", va="center", color=text_color, fontsize=10)

    cbar= plt.colorbar(im, ax=ax)
    cbar.set_label("Probability")

    fig.tight_layout()
    file_path= output_dir / filename
    fig.savefig(file_path, dpi=200, bbox_inches="tight")
    plt.close(fig)

    return file_path

def fidelity_comparison(comparison_dict, output_dir= FIGURES_DIR, filename="fidelity_comparison.png", title="Stage 4: Fidelity Comparison"):
    output_dir= ensure_directory(output_dir)
    branches= list(comparison_dict.keys())
    fidelities= [comparison_dict[branch]["fidelity"] for branch in branches]

    colors= {"ideal": "seagreen", "noisy": "indianred", "calibrated": "steelblue"}
    bar_colors= [colors.get(branch, "gray") for branch in branches]

    fig, ax= plt.subplots(figsize=(7,5))
    bars= ax.bar(branches, fidelities, color=bar_colors)
    ax.set_title(title)
    ax.set_xlabel("Branch")
    ax.set_ylabel("Fidelity")
    ax.set_ylim(0.0, 1.05)
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    for bar, fidelity in zip(bars, fidelities):
        ax.text(bar.get_x() + bar.get_width() / 2,
                fidelity + 0.01,
                f"{fidelity:.4f}",
                ha="center", va="bottom", fontsize=10
               )
        
    fig.tight_layout()
    file_path= output_dir / filename
    fig.savefig(file_path, dpi=200, bbox_inches="tight")
    plt.close(fig)

    return file_path
