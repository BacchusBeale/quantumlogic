import numpy as np
from qiskit import QuantumCircuit, Aer
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
from qiskit.quantum_info import Statevector
from qiskit.quantum_info import Operator

class QComputer():
    def __init__(self, numQubits=1, numBits=1) -> None:
        self.numQubits = numQubits
        self.numBits = numQubits
        if numBits<1:
            self.circuit = QuantumCircuit(self.numQubits)
        else:
            self.circuit = QuantumCircuit(self.numQubits, self.numBits)

        self.job=None
        self.output=None
        self.instructionSet=None

    def resetQubit(self, qubitIndex=0):
        self.instructionSet=self.circuit.reset(qubitIndex)

    def resetQubitRange(self, *qubitList):
        self.instructionSet=self.circuit.reset(qubitList)
        
    def notGate(self, qubitIndex=0):
        self.instructionSet=self.circuit.x(qubitIndex)

    def addBarrier(self):
        self.instructionSet=self.circuit.barrier()

    def addMeasure(self, qubitIndex, bitIndex):
        self.instructionSet=self.circuit.measure(qubitIndex, bitIndex)

    def plotCircuit(self, display=True, saveFile=False, saveAs='circuit.png'):
        self.circuit.draw('mpl')
        if saveFile:
            plt.savefig(saveAs)
        if display:
            plt.show()

    def runSimulator(self, numshots=1):
        # We'll run the program on a simulator
        backend = Aer.get_backend('aer_simulator')
        # Since the output will be deterministic, we can use just a single shot to get it
        self.job = backend.run(self.circuit, shots=numshots, memory=True)
        self.output = self.job.result().get_memory()[0]
        return self.output

    def cNotGate(self, qubitStart, qubitEnd):
        self.instructionSet=self.circuit.cx(control_qubit=qubitStart, target_qubit=qubitEnd)

    def hadamardGate(self, qubitIndex=0):
        self.instructionSet=self.circuit.h(qubit=qubitIndex)