import qsystem
import matplotlib.pyplot as plt

def testCircuit():
    nQubits=3
    nBits=0
    computer = qsystem.QComputer(
        numQubits=nQubits,
        numBits=nBits
    )

    handle = computer.addHadamardGate(
        qubitNumber=0
    )
    handle = computer.addCNotGate(
        qubitFrom=0,
        qubitTo=1
    )

    handle = computer.addCNotGate(
        qubitFrom=0,
        qubitTo=2
    )

    print(handle)

    computer.visualiseCircuit(
        showWindow=True,
        saveAs='ghzstate.png'
    )

    computer.updateStateVector()

    asciiTxt = computer.getStateVectorText(
        useRepr=True,
        saveAs='staterepr.txt'
    )

    print("State vector repr\n")
    print(asciiTxt)
    print("==================\n")

    asciiTxt = computer.getStateVectorText(
        useRepr=False,
        saveAs='statetext.txt'
    )

    print("State vector text\n")
    print(asciiTxt)
    print("==================\n")

    computer.showStateVectorPlot(
        drawType='qsphere',
        show=True,
        saveAs='qsphere.png'
    )

    computer.showStateVectorPlot(
        drawType='bloch',
        show=True,
        saveAs='bloch.png'
    )

    computer.showStateVectorPlot(
        drawType='paulivec',
        show=True,
        saveAs='paulivec.png'
    )

testCircuit()