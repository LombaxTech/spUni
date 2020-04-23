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


# file = open('L7.net')
file = open('testCircuit1.net')
lines = file.readlines()

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
                R = 1 / (1j * 60 * C)

            elif(line[10] == 'L'):
                L = line[12:]
                L = float(L)
                # TODO: Get Resistance value of L

            # print(R)

            # ? nodeTwo = 0 => shunt, else => series

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


# for matrix in matrixList:
#     print(matrix)

resultantMatrix = productOfList(matrixList)
print(resultantMatrix)
