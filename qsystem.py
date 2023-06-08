import numpy as np
from qiskit import QuantumCircuit
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

    def resetQubit(self, qubitIndex=0):
        self.circuit.reset(qubitIndex)
        
    def addNotGate(self, qubitIndex=0):
        self.circuit.x(qubitIndex)

    def addBarrier(self):
        self.circuit.barrier()

    def addMeasure(self, qubitIndex, bitIndex):
        self.circuit.measure(qubitIndex, bitIndex)

    def plotCircuit(self, display=True, saveFile=False, saveAs='circuit.png'):
        self.circuit.draw('mpl')
        if display:
            plt.show()

        if saveFile:
            plt.savefig(saveAs)



        