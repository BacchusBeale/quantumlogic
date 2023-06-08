import qsystem

def makeNotGate():
    nQubits=1
    nBits=1
    qc = qsystem.QComputer(
        numBits=nBits,
        numQubits=nQubits
    )

    qc.resetQubit(qubitIndex=0)
    qc.addNotGate(qubitIndex=0)
    qc.addBarrier()
    qc.addMeasure(qubitIndex=0, bitIndex=0)
    qc.plotCircuit(
        display=True,
        saveAs='notgate.png',
        saveFile=True
    )



makeNotGate()