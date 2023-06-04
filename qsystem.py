import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
from qiskit.quantum_info import Statevector

class QComputer():
    def __init__(self, numQubits=1, numBits=1) -> None:
        self.numQubits = numQubits
        self.numBits = numQubits
        if numBits<1:
            self.qCircuit = QuantumCircuit(self.numQubits)
        else:
            self.qCircuit = QuantumCircuit(self.numQubits, self.numBits)

        self.instructionSet = None
        self.stateVector = None

    def updateStateVector(self):
        print("update state vector")
        # Set the intial state of the simulator to the ground state using from_int
        self.stateVector = Statevector.from_int(0, 2**3)
        # Evolve the state by the quantum circuit
        self.stateVector = self.stateVector.evolve(self.qCircuit)

    # Valid choices are qsphere, hinton, bloch, city, or paulivec.
    def showStateVectorPlot(self, drawType='qsphere', show=False, saveAs=None):
        print(f"show state vector: {drawType}")
        result = self.stateVector.draw(output=drawType)
        
        if saveAs:
            plt.savefig(saveAs)

        if show:
            plt.show()
        return result
    
    # Valid choices are text, repr
    def getStateVectorText(self, useRepr=True, saveAs=None):
        print("getStateVectorText")
        result=""
        if useRepr:
            result = self.stateVector.draw() # repr is default
        else:
            result = self.stateVector.draw(output='text')

        if saveAs:
            with open(saveAs, 'w') as f:
                f.write(result)
        return result

    def addHadamardGate(self, qubitNumber):
        print("Add H gate")
        self.instructionSet = self.qCircuit.h(qubit=qubitNumber)
        return self.instructionSet
    
    def addCNotGate(self, qubitFrom, qubitTo):
        print("Add C Not gate")
        self.instructionSet = self.qCircuit.cnot(
            control_qubit=qubitFrom, 
            target_qubit=qubitTo)
        return self.instructionSet
    
    def visualiseCircuit(self, showWindow=True, saveAs=None):
        print("show circuit")
        
        if saveAs:
            self.qCircuit.draw('mpl', filename=saveAs)
        else:
            self.qCircuit.draw('mpl')

        if showWindow:
            plt.show()
        