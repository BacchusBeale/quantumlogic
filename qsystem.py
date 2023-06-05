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
            self.qCircuit = QuantumCircuit(self.numQubits)
        else:
            self.qCircuit = QuantumCircuit(self.numQubits, self.numBits)

        self.instructionSet = None
        self.stateVector = None
        self.measurementCircuit = None
        self.resultCircuit = None

    def showDataArray(self):
        print("showDataArray")
        U = Operator(self.qCircuit)
        print(U.data)

    def updateStateVector(self, useResultCircuit=False):
        print("update state vector")
        # Set the intial state of the simulator to the ground state using from_int
        self.stateVector = Statevector.from_int(0, 2**3)
        # Evolve the state by the quantum circuit
        if useResultCircuit==False:
            self.stateVector = self.stateVector.evolve(self.qCircuit)
        else:
            if self.resultCircuit is None:
                return False
            
            self.stateVector = self.stateVector.evolve(self.resultCircuit)

        return True

    # Valid choices are qsphere, hinton, bloch, city, or paulivec.
    def showStateVectorPlot(self, drawType='qsphere', show=False, saveAs=None):
        print(f"show state vector: {drawType}")
        if self.stateVector is None:
            return False
        self.stateVector.draw(output=drawType)
        
        if saveAs:
            plt.savefig(saveAs)

        if show:
            plt.show()
        return True
    
    # Valid choices are text, repr
    def getStateVectorText(self, useRepr=True, saveAs=None):
        print("getStateVectorText")
        if self.stateVector is None:
            return False
        
        result = ''
        if useRepr:
            result = self.stateVector.draw() # repr is default
        else:
            result = self.stateVector.draw(output='text')

        if saveAs:
            with open(saveAs, 'w') as f:
                f.write(result)
        return True

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
    
    def addBarrier(self, numQubits):
        self.qCircuit.barrier(range(numQubits))

    def addMeasurement(self, numQubits, numBits):
        print(f"addMeasurement: {numQubits}, {numBits}")
        self.measurementCircuit = QuantumCircuit(numQubits, numBits)
        self.measurementCircuit.measure(range(numQubits), range(numBits))
        self.resultCircuit = self.measurementCircuit.compose(
            self.qCircuit, range(numBits), front=True
        )
    
    def visualiseCircuit(self, showWindow=True, saveAs=None):
        print("show circuit")
        if saveAs:
            self.qCircuit.draw('mpl', filename=saveAs)
        else:
            self.qCircuit.draw('mpl')

        if showWindow:
            plt.show()

    def visualiseResultCircuit(self, showWindow=True, saveAs=None):
        print("show circuit")
        if saveAs:
            self.resultCircuit.draw('mpl', filename=saveAs)
        else:
            self.resultCircuit.draw('mpl')

        if showWindow:
            plt.show()
        