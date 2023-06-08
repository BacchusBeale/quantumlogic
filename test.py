import qsystem

def makeNotGate(numNots=1):
    nQubits=1
    nBits=1
    qc = qsystem.QComputer(
        numBits=nBits,
        numQubits=nQubits
    )

    qc.resetQubit(qubitIndex=0)
    n=numNots
    while n>0:
        qc.addNotGate(qubitIndex=0)
        n-=1

    qc.addBarrier()
    qc.addMeasure(qubitIndex=0, bitIndex=0)
    qc.plotCircuit(
        display=True,
        saveAs='notgate.png',
        saveFile=True
    )

    result = qc.runSimulator()
    print(f"QC result: {result}")

makeNotGate(numNots=2)