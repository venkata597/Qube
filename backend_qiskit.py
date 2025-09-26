from qiskit import QuantumCircuit

def ir_to_qiskit(ir):
    qc = QuantumCircuit(ir["qubits"], ir.get("qubits", 0))  # Classical bits = number of qubits if not specified

    for gate in ir["gates"]:
        g = gate.get("gate")
        if g == "H":
            qc.h(gate["target"])
        elif g == "X":
            qc.x(gate["target"])
        elif g == "CNOT":
            qc.cx(gate["control"], gate["target"])
        elif g == "MEASURE":
            targets = gate.get("target")
            if isinstance(targets, list):
                for i, q in enumerate(targets):
                    qc.measure(q, i)
            else:
                qc.measure(targets, 0)

    return qc
