import numpy as np
import sys

# * FUNCTIONS


def checkIfNumber(input):
    if ((input != 0) and (input != 1) and (input != 2) and (input != 3) and (input != 4) and (input != 5) and (input != 6) and (input != 7) and (input != 8) and (input != 9) and (input != '0') and (input != '1') and (input != '2') and (input != '3') and (input != '4') and (input != '5') and (input != '6') and (input != '7') and (input != '8') and (input != '9') and (input != '.')):
        return False
    else:
        return True


def getPositionOfSpace(startPosition):
    spaceFound = False
    countUntilSpace = 0
    while(spaceFound == False):
        if (checkIfNumber(line[startPosition + countUntilSpace]) == False):
            spaceFound = True
        else:
            countUntilSpace += 1
    return (startPosition + countUntilSpace)


def productOfList(myList):
    product = 1
    for matrix in myList:
        if (type(product) == int):
            product = matrix
        else:
            product = product @ matrix
    return product


file = open('L7.net')
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
                R = line[12:getPositionOfSpace(12)]
                R = float(R)
                # print(R)
            elif(line[10] == 'G'):
                G = line[12:getPositionOfSpace(12)]
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

            # print(R)

# for matrix in matrixList:
#     print(matrix)

resultantMatrix = productOfList(matrixList)
print(resultantMatrix)

# print(productOfList(matrixList))

# def getResultantMatrix(frequency):
#     for line in lines:
#     if (line[0] == '#'):
#         pass
#     else:
#         if ("<CIRCUIT>" in line):
#             circuitSwitch = True

#         elif ("</CIRCUIT" in line):
#             circuitSwitch = False

#         elif (circuitSwitch == True):
#             nodeOne = line[3]
#             nodeTwo = line[8]

#             nodeOne = int(nodeOne)
#             nodeTwo = int(nodeTwo)

#             # !===========================
#             if (line[10] == 'C'):
#                 C = line[12:getPositionOfSpace(12)]
#                 R = 1/j*2*3*frequency
#             # !================================

#             if (line[10] == 'R'):
#                 R = line[12:getPositionOfSpace(12)]
#                 R = float(R)
#                 # print(R)
#             elif(line[10] == 'G'):
#                 G = line[12:getPositionOfSpace(12)]
#                 G = float(G)
#                 R = 1/G
#                 # print('R is:', R, 'G is:', G)

#             # nodeTwo = 0 => shunt, else => series
#             if (nodeTwo == 0):
#                 matrixList.append(np.array([
#                     [1, 0],
#                     [(1/R), 1]
#                 ]).astype(float))
#             else:
#                 matrixList.append(np.array([
#                     [1, R],
#                     [0, 1]
#                 ]).astype(float))
# for frequency in frequencies:
