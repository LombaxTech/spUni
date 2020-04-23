import numpy as np


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


file = open('testCircuit2.net')
lines = file.readlines()

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

            # if (line[10] == 'R'):
            #     R = line[12:getPositionOfSpace(12)]
            #     R = float(R)
            #     print('the value of R is:', R)
            # elif(line[10] == 'G'):
            #     G = line[12:getPositionOfSpace(12)]
            #     G = float(G)
            #     R = 1/G
            #     print('The value of G is:', G, 'and the value of R is:', R)
            if(line[10] == 'C'):
                C = line[12:]
                C = float(C)
                R = 1 / (1j * 60 * C)
                # R = 1 / 1j

                print('C:', C)
                print('R:', R)
                print('Type of C:', type(C))
                print('Type of R:', type(R))

            # nodeTwo = 0 => shunt, else => series
            # if (nodeTwo == 0):
            #     matrixList.append(np.array([
            #         [1, 0],
            #         [(1/R), 1]
            #     ]).astype(float))
            # else:
            #     matrixList.append(np.array([
            #         [1, R],
            #         [0, 1]
            #     ]).astype(float))


# resultantMatrix = productOfList(matrixList)
# print(resultantMatrix)
