import numpy as np
from qiskit import QuantumCircuit, Aer
from qiskit import transpile
from qiskit import QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_state_city
from qiskit.visualization import plot_state_qsphere, plot_bloch_multivector
from qiskit.visualization import plot_bloch_vector
from qiskit.visualization import plot_state_paulivec, plot_state_hinton
import matplotlib.pyplot as plt
from qiskit.quantum_info import Statevector
from qiskit.quantum_info import Operator
from math import pi

CITY=0
QSPHERE=1
BLOCH=2
BLOCH_MULTI=3
PAULIVEC=4
HINTON=5

SIM_UNITARY=0
SIM_AER=1
SIM_QASM=2

class QComputer():

    def __init__(self, numQubits=0, numBits=0) -> None:
        self.qRegisters=None
        self.classicalRegisters=None
        self.circuit = QuantumCircuit()
        if numBits>0 or numQubits>0:
            self.initCircuit(
                numBits=numBits,
                numQubits=numQubits
            )
        self.job=None
        self.output=None
        self.instructionSet=None

    def initCircuit(self, numQubits=0, numBits=0, groupRegisters=False) -> None:
        print("init Q circuit")
        self.numQubits = numQubits
        self.numBits = numQubits
        self.qRegisters = QuantumRegister(size=numQubits)
        self.classicalRegisters = ClassicalRegister(size=numBits)
        if numQubits>0 and numBits<1:
            self.circuit = QuantumCircuit(self.qRegisters)
        elif numQubits>0 and numBits>0:
            self.circuit = QuantumCircuit(self.qRegisters, self.classicalRegisters)
        else:
            self.circuit = QuantumCircuit()

    def phaseGate(self, phase=0, qubitIndex=0):
        self.circuit.p(theta=phase,
                       qubit=qubitIndex)

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
    
    def plotStateVector(self,
                        plotType=CITY,
                        display=True, 
                        saveFile=True, 
                        saveAs='statevector.png'):
        print("plot state vector")
        state=None
        ok=True
        try:
            state = self.stateVector()
            if plotType==CITY:
                plot_state_city(state)
            elif plotType==QSPHERE:
                plot_state_qsphere(state)
            elif plotType==BLOCH:
                plot_bloch_vector(state)
            elif plotType==BLOCH_MULTI:
                plot_bloch_multivector(state)
            elif plotType==PAULIVEC:
                plot_state_paulivec(state)
            elif plotType==HINTON:
                plot_state_hinton(state)
            else:
                ok = False

            if ok:
                if saveFile:
                    plt.savefig(saveAs)

                if display:
                    plt.show()

        except BaseException as e:
            print("Plot error: {e}")
            ok=False
        
        return ok, state

    def runSimulator(self, simType=SIM_UNITARY, numshots=1, display=True, saveFile=True, saveAs='aer.png'):
        # We'll run the program on a simulator
        print("Run simulator")
        ok=True
        try:
            simName='unitary_simulator'
            if simType==SIM_UNITARY:
                simName='unitary_simulator'
            elif simType==SIM_AER:
                simName='aer_simulator'
            elif simType==SIM_QASM:
                simName='qasm_simulator'
            else:
                raise BaseException("Invalid choice")

            backend = Aer.get_backend(simName)
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

        except BaseException as e:
            print(f"Simulator error: {e}")

        return self.output

    def cNotGate(self, qubitStart, qubitEnd):
        self.instructionSet=self.circuit.cx(control_qubit=qubitStart, target_qubit=qubitEnd)

    def hadamardGate(self, qubitIndex=0):
        self.instructionSet=self.circuit.h(qubit=qubitIndex)