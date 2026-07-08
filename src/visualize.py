from pathlib import Path
import matplotlib.pyplot as plt
from qiskit.visualization import plot_state_city

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIGURES_DIR = PROJECT_ROOT / "results" / "figures"

def ensure_directory(path):
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def densitymatrix_plot(density_matrix, state_name, output_dir= FIGURES_DIR):
    output_dir= ensure_directory(output_dir)
    fig = plot_state_city(density_matrix, title= f"Reconstructed density matrix: {state_name}")
    
    for ax in fig.axes:
        if hasattr(ax, 'zaxis'):
            ax.set_zlim(0.0, 1.0)
    file_path= output_dir / f"density_matrix_{state_name}.png"
    fig.savefig(file_path, dpi=200, bbox_inches="tight")
    plt.close(fig)

    return file_path

def fidelity_barchart(summary_rows, output_dir= FIGURES_DIR):
    output_dir= ensure_directory(output_dir)

    states = [row["state"] for row in summary_rows]
    fidelities = [row["fidelity"] for row in summary_rows]

    fig, ax= plt.subplots(figsize=(8,5))
    bars= ax.bar(states, fidelities, color="steelblue")

    ax.set_title("State Tomography Fidelity by Test State")
    ax.set_xlabel("State")
    ax.set_ylabel("Fidelity")
    ax.set_ylim(0.0, 1.05)
    ax.grid(axis="y", linestyle= "--", alpha=0.4)

    for bar, fidelity in zip(bars, fidelities):
        ax.text(bar.get_x() + bar.get_width() / 2, fidelity + 0.01, f"{fidelity:.4f}", ha="center", va="bottom", fontsize= 9)

    fig.tight_layout()
    file_path= output_dir / "fidelity_summary.png"
    fig.savefig(file_path, dpi=200, bbox_inches="tight")
    plt.close(fig)

    return file_path