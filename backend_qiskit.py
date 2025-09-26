from qiskit import QuantumCircuit

def ir_to_qiskit(ir):
    qc = QuantumCircuit(ir["qubits"], len(ir["measurements"]))
    for gate in ir["gates"]:
        if gate[0] == "H":
            qc.h(gate[1])
        elif gate[0] == "X":
            qc.x(gate[1])
        elif gate[0] == "CNOT":
            qc.cx(gate[1], gate[2])

    for i, qubit in enumerate(ir["measurements"]):
        qc.measure(qubit, i)

    return qc
