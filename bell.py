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
        qc.notGate(qubitIndex=0)
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

#makeNotGate(numNots=2)

def bellState():
    nQubits=2
    nBits=2
    q = qsystem.QComputer(
        numBits=nBits,
        numQubits=nQubits
    )
    q.resetQubit(0)
    q.resetQubit(1)
    q.hadamardGate(qubitIndex=0)
    q.cNotGate(qubitStart=0,
               qubitEnd=1)
    
    for i in range(6):
        ok, state = q.plotStateVector(
            plotType=i,
            display=True,
            saveAs=f'beforeMeasure{i}.png',
            saveFile=True
        )
         
        print(f"Success? {ok}")

    q.addBarrier()
    q.addMeasure(0,0)
    q.addMeasure(1,1)

    q.plotCircuit(
        display=True,
        saveAs='bell.png',
        saveFile=True
    )

    output = q.stateVector()
    print(output)

    for i in range(6):
        ok, state = q.plotStateVector(
            plotType=i,
            display=False,
            saveAs=f'afterMeasure{i}.png',
            saveFile=True
        )

        print(f"Success? {ok}")

    answers = []

    result = q.runQasmSimulator(
        numshots=1024,
        saveAs='qasm.png',
        saveFile=True
    )
    
    print(result)
    answers.append(str(result))
    
    txt = ",".join(answers)
    with open('qasm.txt', 'w') as f:
        f.write(txt)

    # answers = []

    # result = q.runAerSimulator(
    #     numshots=1024,
    #     saveAs='aer.png',
    #     saveFile=True
    # )
    
    # print(result)
    # answers.append(str(result))
    
    # txt = ",".join(answers)
    # with open('aer.txt', 'w') as f:
    #     f.write(txt)

bellState()
