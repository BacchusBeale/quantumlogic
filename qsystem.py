import numpy as np
from qiskit import QuantumCircuit, Aer
from qiskit import transpile
from qiskit import QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_state_city
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

    def stateVector(self):
        print("state vector")
        backend = Aer.get_backend('statevector_simulator')
        self.job = backend.run(self.circuit)
        self.output = self.job.result()
        outputstate = self.output.get_statevector(self.circuit, decimals=3)
        return outputstate
    
    def plotStateVector(self, display=True, saveFile=True, saveAs='statevector.png'):
        print("plot state vector")
        state = self.stateVector()
        plot_state_city(state)
        if saveFile:
            plt.savefig(saveAs)

        if display:
            plt.show()

        return state

    def runAerSimulator(self, numshots=1, display=True, saveFile=True, saveAs='aer.png'):
        # We'll run the program on a simulator
        backend = Aer.get_backend('aer_simulator')
        # Since the output will be deterministic, we can use just a single shot to get it
        compile = transpile(self.circuit, backend=backend)
        self.job = backend.run(compile, shots=numshots)
        
        self.output = self.job.result()
        counts = self.output.get_counts()
        plot_histogram(counts)

        if saveFile:
            plt.savefig(saveAs)

        if display:
            plt.show()

        return self.output
    
    def runQasmSimulator(self, numshots=1024, display=True, saveFile=True, saveAs='qasm.png'):
        # We'll run the program on a simulator
        backend = Aer.get_backend('qasm_simulator')
        # Since the output will be deterministic, we can use just a single shot to get it
        compile = transpile(self.circuit, backend=backend)
        self.job = backend.run(compile, shots=numshots)
        
        self.output = self.job.result()
        counts = self.output.get_counts()
        plot_histogram(counts)

        if saveFile:
            plt.savefig(saveAs)
            
        if display:
            plt.show()

        return self.output

    def cNotGate(self, qubitStart, qubitEnd):
        self.instructionSet=self.circuit.cx(control_qubit=qubitStart, target_qubit=qubitEnd)

    def hadamardGate(self, qubitIndex=0):
        self.instructionSet=self.circuit.h(qubit=qubitIndex)