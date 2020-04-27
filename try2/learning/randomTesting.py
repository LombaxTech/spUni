# myString = 'hello world'
# myString = int(myString)
# print(myString)

import numpy as np
import sys

z1 = 1
z2 = 1.0
z3 = 1j
z4 = 5

# print(type(z1))
# print(type(z2))
# print(z3 + z2)
# print(type(z3 + z2))

# print(z4)

# z4 = complex(z4)
# print(z4)

# G = BREXIT
# G = float(G)

# if (type(G) != float):
#     print('some error')
# else:
#     print('no error')

# X = 10.0
# if (type(X) == float):
#     print('is float')
# else:
#     print('not float')


fStart = 10.0
fEnd = 10e+6
nFreqs = 10

# freqs = freqs + [fStart + n*(fEnd - fStart)/(nFreqs-1)]

freqs = [fStart]

for n in range(nFreqs)[1:]:
    freqs = freqs + [fStart + n*(fEnd - fStart)/(nFreqs-1)]

# print(freqs)

# freqs is a list of frequencies

# print(sys.argv)
# file = open(sys.argv[1])


file = open('../testCircuit1.net')
lines = file.readlines()


def productOfList(myList):
    product = 1
    for matrix in myList:
        if (type(product) == int):
            product = matrix
        else:
            product = product @ matrix
    return product


def getMatrix():
    matrixList = []
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
                    # print(R)
                elif(line[10] == 'G'):
                    G = line[12:]
                    G = float(G)
                    R = 1/G
                    # print('R is:', R, 'G is:', G)
                elif(line[10] == 'C'):
                    C = line[12:]
                    C = float(C)
                    R = 1 / (1*j * 2 * 3.14 * frequency * C)

                # nodeTwo = 0 => shunt, else => series
                if (nodeTwo == 0):
                    matrixList.append(np.array([
                        [1, 0],
                        [(1/R), 1]
                    ]).astype(float))
                else:
                    matrixList.append(np.array([
                        [1, R],
                        [0, 1]
                    ]).astype(float))

    resultantMatrix = productOfList(matrixList)
    # print(resultantMatrix)


frequencyList = [10, 100, 1000]

for frequency in frequencyList:
    matrix = getMatrix()
    # TODO: Figure out Vin, Vout,

# print(np.conj(10 + 6j))

randomList = []

randomList.append('item1')

print(randomList)
