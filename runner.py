from qiskit import Aer, execute
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
from backend_qiskit import build_circuit

def run(ir):
    print("\n[ IR Representation ]")
    print(ir)

    qc = build_circuit(ir)
    print("\n[ Circuit Diagram ]")
    print(qc.draw())

    backend = Aer.get_backend("aer_simulator")
    job = execute(qc, backend, shots=ir["shots"])
    result = job.result()
    counts = result.get_counts()

    print("\n[ Measurement Results ]")
    print(counts)

    qc.draw("mpl")
    plt.show()
    
