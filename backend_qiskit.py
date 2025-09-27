from qiskit import QuantumCircuit

def build_circuit(ir):
    num_qubits = ir["qubits"]
    num_clbits = len(ir["measurements"])
    qc = QuantumCircuit(num_qubits, num_clbits)

    # Apply gates
    for gate in ir["gates"]:
        if gate[0] == "H":
            qc.h(gate[1])
        elif gate[0] == "X":
            qc.x(gate[1])
        elif gate[0] == "CNOT":
            qc.cx(gate[1], gate[2])
        else:
            raise ValueError(f"Unknown gate: {gate}")

    # Apply measurements
    for i, q in enumerate(ir["measurements"]):
        qc.measure(q, i)

    return qc
