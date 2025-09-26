from qiskit import Aer, execute
import matplotlib.pyplot as plt
from backend_qiskit import ir_to_qiskit

def run(ir):
    qc = ir_to_qiskit(ir)

    backend = Aer.get_backend("qasm_simulator")
    job = execute(qc, backend, shots=ir.get("shots", 1024))
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
