import numpy as np

# * FUNCTIONS


def productOfList(myList):
    product = 1
    for matrix in myList:
        if (type(product) == int):
            product = matrix
        else:
            product = product @ matrix
    return product


file = open('testCircuit1.net')
lines = file.readlines()


def getResultantMatrix(frequency):
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
                    # print('Value of R:', R)

                elif(line[10] == 'G'):
                    G = line[12:]
                    G = float(G)
                    R = 1/G
                    # print('Value of G:', G, 'Value of R:', R)
                    # TODO: Handle error if value is BREXIT for example

                elif(line[10] == 'C'):
                    C = line[12:]
                    C = float(C)
                    R = 1 / (1j * 2 * 3.14 * frequency * C)

                elif(line[10] == 'L'):
                    L = line[12:]
                    L = float(L)
                    R = 1j * 2 * 3.14 * frequency * L

                # print(R)

                # ? nodeTwo = 0 => shunt, else => series

                if (nodeTwo == 0):
                    matrixList.append(np.array([
                        [1, 0],
                        [(1/R), 1]
                    ]).astype(complex))
                else:
                    matrixList.append(np.array([
                        [1, R],
                        [0, 1]
                    ]).astype(complex))

    resultantMatrix = productOfList(matrixList)
    return resultantMatrix


matrixOne = getResultantMatrix(10)
print(matrixOne)

Vin = []
Vout = []
Iin = []
Av = []

frequencyList = [10, 15, 20, 25, 30]

for frequency in frequencyList:
    matrix = getResultantMatrix(frequency)
    Bn = matrix[0, 1]
    Av = Av + [50*Bn]

# ? Rinput = 50
# ? Av = Rinput * Bn

# * GET MATRIX => FIGURE OUT OTHER VALUES


# Lists for each variable output
# zOutList = []
# zIn = []
# # ...

# for f in freqs:
#     matrix = getResultantMatrix(f)
#     # extracted values out of the matrix
#     A = matrix[0]
#     # B = ..

#     Vin = ...
#     VinList.append(Vin)
#     Vout = ...
#     VoutList.append(VoutList))


# zOutList=[12, 2, 2 3, 33, 3]
# zIn=[]


# # TODO: OUTPUTTING - FINAL STEP
