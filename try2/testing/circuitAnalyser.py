import sys
import numpy as np

inputFile = sys.argv[1]
outputFileName = sys.argv[2]

try:

    # * FUNCTION TO GET THE PRODUCT OF A LIST OF MATRICES

    def productOfList(myList):
        product = 1
        for matrix in myList:
            if (type(product) == int):
                product = matrix
            else:
                product = product @ matrix
        return product

    # * READING INPUT FILE AND DEFINING OUTPUT FILE

    file = open(inputFile)
    lines = file.readlines()

    # for line in lines:
    #     position = line.find('File_name')
    #     if (position != -1):
    #         outputFileName = line[12:]
    #         outputFileName = outputFileName[:-1]

    # try:
    #     outputFileName
    # except:
    #     inputFile = inputFile[:-4]
    #     outputFileName = inputFile + '.out'

    # * FUNCTION TO GET RESULTANT MATRIX AT A PARTICULAR FREQUENCY

    def getResultantMatrix(frequency):
        toBeSortedList = []
        circuitSwitch = False

        for line in lines:
            if (line[0] == '#'):
                pass
            else:
                if ("<CIRCUIT>" in line):
                    circuitSwitch = True

                elif ("</CIRCUIT>" in line):
                    circuitSwitch = False

                elif (circuitSwitch == True):
                    nodeOne = line[3]
                    nodeTwo = line[8]

                    nodeOne = int(nodeOne)
                    nodeTwo = int(nodeTwo)

                    if (line[10] == 'R'):
                        R = line[12:]
                        R = float(R)

                    elif(line[10] == 'G'):
                        G = line[12:]
                        G = float(G)
                        R = 1/G

                    elif(line[10] == 'C'):
                        C = line[12:]
                        C = float(C)
                        R = 1 / (1j * 2 * 3.14 * frequency * C)

                    elif(line[10] == 'L'):
                        L = line[12:]
                        L = float(L)
                        R = 1j * 2 * 3.14 * frequency * L

                    # ? nodeTwo = 0 => shunt, else => series

                    if (nodeTwo == 0):
                        toBeSortedList.append({
                            'nodeOne': nodeOne,
                            'matrix': np.array([
                                [1, 0],
                                [(1/R), 1]
                            ]).astype(complex)
                        })
                    else:
                        toBeSortedList.append({
                            'nodeOne': nodeOne,
                            'matrix': np.array([
                                [1, R],
                                [0, 1]
                            ]).astype(complex)
                        })

        sortedList = sorted(toBeSortedList, key=lambda i: i['nodeOne'])
        sortedMatrixList = []

        for obj in sortedList:
            sortedMatrixList.append(obj['matrix'])

        resultantMatrix = productOfList(sortedMatrixList)
        return resultantMatrix

    # * GETTING THE FREQUENCIES IN THE FILE

    termsSwitch = False

    # ? This gets the value of nFreqs

    for line in lines:
        if (line[0] == '#'):
            pass
        else:
            if ("<TERMS>" in line):
                termsSwitch = True

            elif ("</TERMS>" in line):
                termsSwitch = False

            elif (termsSwitch == True):
                position = line.find('Nfreqs')
                if (position != -1):
                    # print(line[position + 7:])
                    nFreqs = line[position + 7:]
                    nFreqs = int(nFreqs)

    fStart = 10.0
    fEnd = 10e+6
    gap = (fEnd - fStart)/(nFreqs - 1)

    # ? generates a list of frequencies
    frequencyList = []

    for n in range(nFreqs):
        frequencyList = frequencyList + [fStart + n*gap]

    # * GET THE VALUES IN THE <TERMS> BLOCK

    termSwitch = False

    RS = 0
    GS = 0

    for line in lines:
        if (line[0] == '#'):
            pass
        else:
            if ("<TERMS>" in line):
                termSwitch = True

            elif ("</TERMS>" in line):
                termSwitch = False

            elif (termSwitch == True):
                position = line.find('VT')
                if (position != -1):
                    VT = line[position + 3: position + 5]
                    VT = float(VT)

                position = line.find('RS')
                if (position != -1):
                    RS = line[position + 3:]
                    RS = float(RS)

                position = line.find('GS')
                if (position != -1):
                    GS = line[position + 3:]
                    GS = float(GS)
                    RS = 1/GS

                position = line.find('RL')
                if (position != -1):
                    RL = line[position + 3:]
                    RL = float(RL)

    # print(VT)
    # print(RS)
    # print(RL)

    # if (GS != 0):
    #     print(GS)
    # if (RS != 0):
    #     print(RS)

    # * CALCULATE MATRIX AND GET VALUES OF CIRCUIT AT EACH FREQUENCY

    valuesObjectList = []

    for frequency in frequencyList:
        resultantMatrix = getResultantMatrix(frequency)

        A = resultantMatrix[0, 0]
        B = resultantMatrix[0, 1]
        C = resultantMatrix[1, 0]
        D = resultantMatrix[1, 1]

        Zout = (D*RS + B) / (C*RS + A)
        Zin = (A*RL + B) / (C*RL + D)
        Av = 1 / (A + (B/RL))
        Ai = 1 / (C*RL + D)
        Vin = (VT*Zin) / (Zin + RS)
        Vout = Vin * Av
        Iin = VT / (Zin + RS)
        Iout = Iin * Ai
        Pin = Vin * np.conj(Iin)
        Pout = Vout * np.conj(Iout)
        Ap = Av * np.conj(Ai)

        values = {
            'frequency': frequency,
            'Vin': Vin,
            'Vout': Vout,
            'Iin': Iin,
            'Iout': Iout,
            'Pin': Pin,
            'Zout': Zout,
            'Pout': Pout,
            'Zin': Zin,
            'Av': Av,
            'Ai': Ai
        }

        valuesObjectList.append(values)

    # TODO: handle errors

    # TODO: handle for when node value exceeds 10

    # * WRITING TO THE OUTPUT FILE

    outputFile = open(outputFileName, 'w')

    outputFile.write('      Freq           Vin                   Vout                    Iin                   Iout                    Pin                   Zout                   Pout                    Zin                     Av                     Ai          ')
    outputFile.write('\n        Hz             V                      V                      A                      A                      W                   Ohms                      W                   Ohms                      L                      L          ')

    for valuesObject in valuesObjectList:

        outputFile.write('\n')

        for key in valuesObject:

            realPart = valuesObject[key].real
            imaginaryPart = valuesObject[key].imag

            realPart = '%.3e' % realPart
            imaginaryPart = '%.3e' % imaginaryPart

            if (key == 'frequency'):
                outputFile.write(' ' + realPart)
            else:
                # * IMAGINARY POSITIVE & REAL POSITIVE
                if ((float(imaginaryPart) >= 0) and (float(realPart) >= 0)):
                    outputFile.write('  ' + realPart + '+j ' + imaginaryPart)

                # * IMAGINARY NEGATIVE & REAL POSTIVE
                elif((float(imaginaryPart) < 0) and (float(realPart) >= 0)):
                    outputFile.write('  ' + realPart + '+j' + imaginaryPart)

                # * IMAGINARY POSITIVE & REAL NEGATIVE
                if ((float(imaginaryPart) >= 0) and (float(realPart) < 0)):
                    outputFile.write(' ' + realPart + '+j ' + imaginaryPart)

                # * IMAGINARY NEGATIVE & REAL NEGATIVE
                elif((float(imaginaryPart) < 0) and (float(realPart) < 0)):
                    outputFile.write(' ' + realPart + '+j' + imaginaryPart)

    print('successfully ran')
    print('damn')
except Exception as err:
    outputFile = open(outputFileName, 'w')
    outputFile.write('')
