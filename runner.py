from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram
from backend_qiskit import ir_to_qiskit
from IPython.display import display

def run(ir):
    qc = ir_to_qiskit(ir)

    simulator = AerSimulator()
    shots = ir.get("shots", 1024)
    job = simulator.run(qc, shots=shots)
    result = job.result()
    counts = result.get_counts()

    print("\n--- Intermediate Representation (IR) ---")
    print(ir)
    print("\n--- Quantum Circuit ---")
    print(qc)
    print("\n--- Execution Results ---")
    print(counts)

    qc.draw("mpl")
    plt.show()
    
    fig = plot_histogram(counts)
    display(fig)